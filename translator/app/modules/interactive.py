'''
This file is a modified version of `interactive.py` found in the github repo for
Fairseq, at https://github.com/pytorch/fairseq

Last modified on 5th July 2019 by Sharad Duwal <[sharad] [.] [duwal] [at] [gmail] [dot] [com]> 

Below is the license this modification is done under.

BSD License

For fairseq software

Copyright (c) 2017-present, Facebook, Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

 * Neither the name Facebook nor the names of its contributors may be used to
    endorse or promote products derived from this software without specific
       prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

from collections import namedtuple

import torch

from fairseq import checkpoint_utils, options, tasks, utils

Batch = namedtuple('Batch', 'ids src_tokens src_lengths')
Translation = namedtuple('Translation', 'src_str hypos pos_scores alignments')

def make_batches(lines, args, task, max_positions, encode_fn):
    tokens = [
        task.source_dictionary.encode_line(
            encode_fn(src_str), add_if_not_exist=False
        ).long()
        for src_str in lines
    ]
    lengths = torch.LongTensor([t.numel() for t in tokens])
    itr = task.get_batch_iterator(
        dataset=task.build_dataset_for_inference(tokens, lengths),
        max_tokens=args.max_tokens,
        max_sentences=args.max_sentences,
        max_positions=max_positions,
    ).next_epoch_itr(shuffle=False)
    for batch in itr:
        yield Batch(
            ids=batch['id'],
            src_tokens=batch['net_input']['src_tokens'], src_lengths=batch['net_input']['src_lengths'],
        )

class Generator():
    def __init__(self, data_path, checkpoint_path="checkpoint_best.pt"):
        self.parser = options.get_generation_parser(interactive=True)
        self.parser.set_defaults(path=checkpoint_path,
            remove_bpe="sentencepiece", dataset_impl="lazy", num_wokers=5
        )
        self.args = options.parse_args_and_arch(self.parser, 
            input_args=[data_path]
        )

        utils.import_user_module(self.args)

        if self.args.buffer_size < 1:
            self.args.buffer_size = 1
        if self.args.max_tokens is None and self.args.max_sentences is None:
            self.args.max_sentences = 1

        assert not self.args.sampling or self.args.nbest == self.args.beam, \
            '--sampling requires --nbest to be equal to --beam'
        assert not self.args.max_sentences or self.args.max_sentences <= self.args.buffer_size, \
            '--max-sentences/--batch-size cannot be larger than --buffer-size'

        self.use_cuda = torch.cuda.is_available() and not self.args.cpu

        self.task = tasks.setup_task(self.args)

        self.models, self._model_args = checkpoint_utils.load_model_ensemble(
            self.args.path.split(':'),
            arg_overrides=eval(self.args.model_overrides),
            task=self.task,
        )

        self.src_dict = self.task.source_dictionary
        self.tgt_dict = self.task.target_dictionary

        for model in self.models:
            model.make_generation_fast_(
                beamable_mm_beam_size=None if self.args.no_beamable_mm else self.args.beam,
                need_attn=self.args.print_alignment,
            )
            if self.args.fp16:
                model.half()
            if self.use_cuda:
                model.cuda()

        self.generator = self.task.build_generator(self.args)

        if self.args.remove_bpe == 'gpt2':
            from fairseq.gpt2_bpe.gpt2_encoding import get_encoder
            self.decoder = get_encoder(
                'fairseq/gpt2_bpe/encoder.json',
                'fairseq/gpt2_bpe/vocab.bpe',
            )
            self.encode_fn = lambda x: ' '.join(map(str, self.decoder.encode(x)))
        else:
            self.decoder = None
            self.encode_fn = lambda x: x

        self.align_dict = utils.load_align_dict(self.args.replace_unk)

        self.max_positions = utils.resolve_max_positions(
            self.task.max_positions(),
            *[model.max_positions() for model in self.models]
        )

    def generate(self, string):
        start_id = 0
        inputs = [string]
        results = []
        for batch in make_batches(inputs, self.args, self.task, self.max_positions, self.encode_fn):
            src_tokens = batch.src_tokens
            src_lengths = batch.src_lengths
            if self.use_cuda:
                src_tokens = src_tokens.cuda()
                src_lengths = src_lengths.cuda()

            sample = {
                'net_input': {
                    'src_tokens': src_tokens,
                    'src_lengths': src_lengths,
                },
            }
            translations = self.task.inference_step(self.generator, self.models, sample)
            for i, (id, hypos) in enumerate(zip(batch.ids.tolist(), translations)):
                src_tokens_i = utils.strip_pad(src_tokens[i], self.tgt_dict.pad())
                results.append((start_id + id, src_tokens_i, hypos))

        for id, src_tokens, hypos in sorted(results, key=lambda x: x[0]):
            if self.src_dict is not None:
                src_str = self.src_dict.string(src_tokens, self.args.remove_bpe)

            for hypo in hypos[:min(len(hypos), self.args.nbest)]:
                hypo_tokens, hypo_str, alignment = utils.post_process_prediction(
                    hypo_tokens=hypo['tokens'].int().cpu(),
                    src_str=src_str,
                    alignment=hypo['alignment'].int().cpu() if hypo['alignment'] is not None else None,
                    align_dict=self.align_dict,
                    tgt_dict=self.tgt_dict,
                    remove_bpe=self.args.remove_bpe,
                )
                if self.decoder is not None:
                    hypo_str = self.decoder.decode(map(int, hypo_str.strip().split()))

                return hypo_str

if __name__ == '__main__':
    gen = Generator("../ne_en_bpe20000/", "../models/ne-en.pt")

    print(gen.generate("▁यस ▁धारा ▁सं बद्ध ▁नाटक हरूमा ▁कथ ्य ▁र ▁शि ल्प ▁दुबै को ▁नयाँ ▁प्रया े ग ▁पाइन्छ ▁।"))