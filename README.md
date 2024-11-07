# tune-nix-eval

Runs Nix evaluation on the given attribute path on a flake reference with a variety of `malloc` replacements.

Uses Optuna to tune the evaluation process.

TODO:

- Add ability to tune zram.
- Package optuna-dashboard.

Example CLI:

```console
$ nix run .# -- --help
usage: tune-nix-eval [-h] [--num-trials NUM_TRIALS] [--num-evals NUM_EVALS] [--eval-timeout EVAL_TIMEOUT] [--allow-turbo] [--tune-store] --flakeref FLAKEREF --attr-path ATTR_PATH [ATTR_PATH ...]

Runs a nix eval using various malloc replacements.

options:
  -h, --help            show this help message and exit
  --num-trials NUM_TRIALS
                        Number of trials
  --num-evals NUM_EVALS
                        Max number of evaluations per trial
  --eval-timeout EVAL_TIMEOUT
                        Timeout for each evaluation, in seconds. Note that this is wall time, not CPU time as reported by Nix.
  --allow-turbo         Allow the CPU to boost its frequency. Recommended to disable for consistent results.
  --tune-store          Test both with and without the Nix daemon. Requires the current user to own the Nix store!
  --flakeref FLAKEREF   Reference to a flake
  --attr-path ATTR_PATH [ATTR_PATH ...]
                        Attribute to evaluate
```

<details><summary>Example run</summary>

```console
[connorbaker@nixos-desktop:~/tune-nix-eval]$ nix run .# -- --allow-turbo --num-trials 100 --num-evals 8 --flakeref "github:ConnorBaker/nixos-configs" --attr-path nixosConfigurations nixos-desktop config system build toplevel
INFO     Setting up artifact directory                                                                                                                                                                                                              main.py:233
INFO     Building memory allocators                                                                                                                                                                                                                 main.py:238
INFO     Building mimalloc                                                                                                                                                                                                             memory_allocators.py:129
INFO     Building .#mimalloc^*                                                                                                                                                                                                                        raw.py:29
INFO     Built mimalloc to /nix/store/0qkj4f520bs77hz5qymcj5fib93idjlk-mimalloc-2.1.7                                                                                                                                                  memory_allocators.py:131
INFO     Building graphene-hardened                                                                                                                                                                                                    memory_allocators.py:129
INFO     Building .#graphene-hardened-malloc^*                                                                                                                                                                                                        raw.py:29
INFO     Built graphene-hardened to /nix/store/k1sngqnf9f0r0rrj8p5vk9sip91lpm5m-graphene-hardened-malloc-2024040900                                                                                                                    memory_allocators.py:131
INFO     Building hoard                                                                                                                                                                                                                memory_allocators.py:129
INFO     Building .#hoard^*                                                                                                                                                                                                                           raw.py:29
INFO     Built hoard to /nix/store/3y22w2j9zyqqwhw3jlzw2syhpjc1zqjb-hoard-3.13-unstable-2024-08-02                                                                                                                                     memory_allocators.py:131
INFO     Building tcmalloc                                                                                                                                                                                                             memory_allocators.py:129
INFO     Building .#gperftools^*                                                                                                                                                                                                                      raw.py:29
INFO     Built tcmalloc to /nix/store/yv9426dy6yvgi5wd8gf889nc9yspf04k-gperftools-2.15                                                                                                                                                 memory_allocators.py:131
INFO     Building libc                                                                                                                                                                                                                 memory_allocators.py:129
INFO     Building .#glibc^*                                                                                                                                                                                                                           raw.py:29
INFO     Built libc to /nix/store/3bvxjkkmwlymr0fssczhgi39c3aj1l7i-glibc-2.40-36                                                                                                                                                       memory_allocators.py:131
INFO     Building scudo-19                                                                                                                                                                                                             memory_allocators.py:129
INFO     Building .#llvmPackages_19.compiler-rt^*                                                                                                                                                                                                     raw.py:29
INFO     Built scudo-19 to /nix/store/iiq6s7s4yy8y5n6bnm1aqvz4jm77wbyn-compiler-rt-libc-19.1.1                                                                                                                                         memory_allocators.py:131
INFO     Building jemalloc                                                                                                                                                                                                             memory_allocators.py:129
INFO     Building .#jemalloc^*                                                                                                                                                                                                                        raw.py:29
INFO     Built jemalloc to /nix/store/fkpxivzalcwimyjzb9f47hz54z74g83q-jemalloc-5.3.0                                                                                                                                                  memory_allocators.py:131
INFO     Building graphene-hardened-light                                                                                                                                                                                              memory_allocators.py:129
INFO     Building .#graphene-hardened-malloc^*                                                                                                                                                                                                        raw.py:29
INFO     Built graphene-hardened-light to /nix/store/k1sngqnf9f0r0rrj8p5vk9sip91lpm5m-graphene-hardened-malloc-2024040900                                                                                                              memory_allocators.py:131
INFO     Warming up                                                                                                                                                                                                                                 main.py:242
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
/nix/store/frzlmcxs16s6r5wwwha6s1pnvz3b3cwc-python3.12-tune_nix_eval-0.1.0/lib/python3.12/site-packages/tune_nix_eval/cmd/main.py:250: ExperimentalWarning: WilcoxonPruner is experimental (supported from v3.6.0). The interface can change in the future.
  pruner=WilcoxonPruner(p_threshold=0.1, n_startup_steps=0),
/nix/store/frzlmcxs16s6r5wwwha6s1pnvz3b3cwc-python3.12-tune_nix_eval-0.1.0/lib/python3.12/site-packages/tune_nix_eval/cmd/main.py:252: ExperimentalWarning: BruteForceSampler is experimental (supported from v3.1.0). The interface can change in the future.
  sampler=BruteForceSampler(seed=42),
[I 2024-11-07 05:22:29,624] A new study created in RDB with name: nix-eval
INFO     A new study created in RDB with name: nix-eval                                                                                                                                                                                          storage.py:286
INFO     Adding baseline trial                                                                                                                                                                                                                      main.py:255
INFO     Running trial 0 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'system'}                                                                                                                                                     main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 6 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 7 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 8 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-0-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:23:02,015] Trial 0 finished with value: 4.8765963315963745 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'system'}. Best is trial 0 with value: 4.8765963315963745.
INFO     Trial 0 finished with value: 4.8765963315963745 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'system'}. Best is trial 0 with value: 4.8765963315963745.                                                                   study.py:1135
INFO     Building .#gperftools^*                                                                                                                                                                                                                      raw.py:29
INFO     Running trial 1 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'tcmalloc'}                                                                                                                                                   main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 6 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 7 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 8 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-1-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:23:35,857] Trial 1 finished with value: 4.876363158226013 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'tcmalloc'}. Best is trial 1 with value: 4.876363158226013.
INFO     Trial 1 finished with value: 4.876363158226013 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'tcmalloc'}. Best is trial 1 with value: 4.876363158226013.                                                                   study.py:1135
INFO     Building .#glibc^*                                                                                                                                                                                                                           raw.py:29
INFO     Running trial 2 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'libc'}                                                                                                                                                       main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 6 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 7 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 8 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-2-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:24:08,501] Trial 2 finished with value: 4.875941753387451 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'libc'}. Best is trial 2 with value: 4.875941753387451.
INFO     Trial 2 finished with value: 4.875941753387451 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'libc'}. Best is trial 2 with value: 4.875941753387451.                                                                       study.py:1135
INFO     Building .#graphene-hardened-malloc^*                                                                                                                                                                                                        raw.py:29
INFO     Running trial 3 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'graphene-hardened'}                                                                                                                                          main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 6.91s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 6.93s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 6.90s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 6.94s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 3 per pruner's suggestion                                                                                                                                                                                                    main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-3-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:24:33,198] Trial 3 finished with value: 6.919162273406982 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'graphene-hardened'}. Best is trial 2 with value: 4.875941753387451.
INFO     Trial 3 finished with value: 6.919162273406982 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'graphene-hardened'}. Best is trial 2 with value: 4.875941753387451.                                                          study.py:1135
INFO     Running trial 4 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'system'}                                                                                                                                                      main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 6 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.86s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 7 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 8 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-4-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:24:57,514] Trial 4 finished with value: 3.867915630340576 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'system'}. Best is trial 4 with value: 3.867915630340576.
INFO     Trial 4 finished with value: 3.867915630340576 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'system'}. Best is trial 4 with value: 3.867915630340576.                                                                      study.py:1135
INFO     Building .#mimalloc^*                                                                                                                                                                                                                        raw.py:29
INFO     Running trial 5 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'mimalloc'}                                                                                                                                                    main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.86s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 6 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 7 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 8 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-5-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:25:22,232] Trial 5 finished with value: 3.869566798210144 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'mimalloc'}. Best is trial 4 with value: 3.867915630340576.
INFO     Trial 5 finished with value: 3.869566798210144 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'mimalloc'}. Best is trial 4 with value: 3.867915630340576.                                                                    study.py:1135
INFO     Building .#gperftools^*                                                                                                                                                                                                                      raw.py:29
INFO     Running trial 6 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'tcmalloc'}                                                                                                                                                    main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.86s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 6 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 7 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 8 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.86s                                                                                                                                                                                                               raw.py:175
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-6-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:25:46,848] Trial 6 finished with value: 3.8663830757141113 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'tcmalloc'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 6 finished with value: 3.8663830757141113 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'tcmalloc'}. Best is trial 6 with value: 3.8663830757141113.                                                                  study.py:1135
INFO     Building .#hoard^*                                                                                                                                                                                                                           raw.py:29
INFO     Running trial 7 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'hoard'}                                                                                                                                                      main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 7 per pruner's suggestion                                                                                                                                                                                                    main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-7-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:26:07,376] Trial 7 finished with value: 5.880383729934692 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'hoard'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 7 finished with value: 5.880383729934692 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'hoard'}. Best is trial 6 with value: 3.8663830757141113.                                                                     study.py:1135
INFO     Building .#graphene-hardened-malloc^*                                                                                                                                                                                                        raw.py:29
INFO     Running trial 8 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'graphene-hardened-light'}                                                                                                                                     main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 8 per pruner's suggestion                                                                                                                                                                                                    main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-8-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:26:23,882] Trial 8 finished with value: 4.879421830177307 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'graphene-hardened-light'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 8 finished with value: 4.879421830177307 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'graphene-hardened-light'}. Best is trial 6 with value: 3.8663830757141113.                                                    study.py:1135
INFO     Building .#jemalloc^*                                                                                                                                                                                                                        raw.py:29
INFO     Running trial 9 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'jemalloc'}                                                                                                                                                    main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 9 per pruner's suggestion                                                                                                                                                                                                    main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-9-eval-results.json                                                                                                                                                                                   main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:26:43,401] Trial 9 finished with value: 4.870158910751343 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'jemalloc'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 9 finished with value: 4.870158910751343 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'jemalloc'}. Best is trial 6 with value: 3.8663830757141113.                                                                   study.py:1135
INFO     Building .#hoard^*                                                                                                                                                                                                                           raw.py:29
INFO     Running trial 10 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'hoard'}                                                                                                                                                      main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 10 per pruner's suggestion                                                                                                                                                                                                   main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-10-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:26:59,874] Trial 10 finished with value: 4.870832681655884 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'hoard'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 10 finished with value: 4.870832681655884 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'hoard'}. Best is trial 6 with value: 3.8663830757141113.                                                                     study.py:1135
INFO     Building .#graphene-hardened-malloc^*                                                                                                                                                                                                        raw.py:29
INFO     Running trial 11 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'graphene-hardened-light'}                                                                                                                                   main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.89s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 11 per pruner's suggestion                                                                                                                                                                                                   main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-11-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:27:20,401] Trial 11 finished with value: 5.880449652671814 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'graphene-hardened-light'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 11 finished with value: 5.880449652671814 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'graphene-hardened-light'}. Best is trial 6 with value: 3.8663830757141113.                                                  study.py:1135
INFO     Building .#glibc^*                                                                                                                                                                                                                           raw.py:29
INFO     Running trial 12 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'libc'}                                                                                                                                                       main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.86s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 5 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 6 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 7 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.86s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 8 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 3.87s                                                                                                                                                                                                               raw.py:175
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-12-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:27:44,960] Trial 12 finished with value: 3.8671215772628784 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'libc'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 12 finished with value: 3.8671215772628784 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'libc'}. Best is trial 6 with value: 3.8663830757141113.                                                                     study.py:1135
INFO     Building .#llvmPackages_19.compiler-rt^*                                                                                                                                                                                                     raw.py:29
INFO     Running trial 13 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'scudo-19'}                                                                                                                                                  main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.88s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 13 per pruner's suggestion                                                                                                                                                                                                   main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-13-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:28:05,592] Trial 13 finished with value: 5.878894805908203 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'scudo-19'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 13 finished with value: 5.878894805908203 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'scudo-19'}. Best is trial 6 with value: 3.8663830757141113.                                                                 study.py:1135
INFO     Building .#llvmPackages_19.compiler-rt^*                                                                                                                                                                                                     raw.py:29
INFO     Running trial 14 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'scudo-19'}                                                                                                                                                   main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 14 per pruner's suggestion                                                                                                                                                                                                   main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-14-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:28:22,230] Trial 14 finished with value: 4.877475380897522 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'scudo-19'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 14 finished with value: 4.877475380897522 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'scudo-19'}. Best is trial 6 with value: 3.8663830757141113.                                                                  study.py:1135
INFO     Building .#jemalloc^*                                                                                                                                                                                                                        raw.py:29
INFO     Running trial 15 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'jemalloc'}                                                                                                                                                  main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 15 per pruner's suggestion                                                                                                                                                                                                   main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-15-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:28:38,711] Trial 15 finished with value: 4.874691605567932 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'jemalloc'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 15 finished with value: 4.874691605567932 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'jemalloc'}. Best is trial 6 with value: 3.8663830757141113.                                                                 study.py:1135
INFO     Building .#mimalloc^*                                                                                                                                                                                                                        raw.py:29
INFO     Running trial 16 with parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'mimalloc'}                                                                                                                                                  main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.87s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 4.88s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 16 per pruner's suggestion                                                                                                                                                                                                   main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-16-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:28:55,329] Trial 16 finished with value: 4.874635100364685 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'mimalloc'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 16 finished with value: 4.874635100364685 and parameters: {'gc_dont_gc': 'false', 'memory_allocator': 'mimalloc'}. Best is trial 6 with value: 3.8663830757141113.                                                                 study.py:1135
INFO     Building .#graphene-hardened-malloc^*                                                                                                                                                                                                        raw.py:29
INFO     Running trial 17 with parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'graphene-hardened'}                                                                                                                                          main.py:190
INFO     Running evaluation 1 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.90s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 2 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.90s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 3 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.91s                                                                                                                                                                                                               raw.py:175
INFO     Running evaluation 4 of 8                                                                                                                                                                                                                  main.py:194
INFO     Evaluating github:ConnorBaker/nixos-configs#nixosConfigurations.nixos-desktop.config.system.build.toplevel                                                                                                                                  raw.py:121
INFO     Evaluation completed in 5.90s                                                                                                                                                                                                               raw.py:175
INFO     Pruning trial 17 per pruner's suggestion                                                                                                                                                                                                   main.py:215
INFO     Generating statistics                                                                                                                                                                                                                      main.py:160
INFO     Creating artifact                                                                                                                                                                                                                          main.py:163
INFO     Saving statistics to artifacts/trial-17-eval-results.json                                                                                                                                                                                  main.py:167
INFO     Uploading artifact                                                                                                                                                                                                                         main.py:170
[I 2024-11-07 05:29:15,928] Trial 17 finished with value: 5.903496503829956 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'graphene-hardened'}. Best is trial 6 with value: 3.8663830757141113.
INFO     Trial 17 finished with value: 5.903496503829956 and parameters: {'gc_dont_gc': 'true', 'memory_allocator': 'graphene-hardened'}. Best is trial 6 with value: 3.8663830757141113.                                                         study.py:1135
{'gc_dont_gc': 'true', 'memory_allocator': 'tcmalloc'}
```

</details>

<details><summary>Example serialized trial result (trial 6 from previous, prettified so it's easier to look at)</summary>

```json
{
  "results": [
    {
      "nix_stats": {
        "cpu_time": 1.9783289432525635,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 1.9783289432525635,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 8146944,
            "vms": 51441664,
            "uss": 6078464,
            "pss": 7272448,
            "swap": 0
          },
          "time": 0.8499505519866943
        },
        {
          "cpu": {
            "user": 0.73,
            "system": 0.16,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 6836,
            "write_count": 7070,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20789617,
            "write_chars": 11178074
          },
          "memory": {
            "rss": 644587520,
            "vms": 710782976,
            "uss": 638554112,
            "pss": 641197056,
            "swap": 0
          },
          "time": 1.854543924331665
        },
        {
          "cpu": {
            "user": 1.41,
            "system": 0.35,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 12818,
            "write_count": 17059,
            "read_bytes": 33249794,
            "write_bytes": 0,
            "read_chars": 39881032,
            "write_chars": 28058215
          },
          "memory": {
            "rss": 1314889728,
            "vms": 1395888128,
            "uss": 1309077504,
            "pss": 1311720448,
            "swap": 0
          },
          "time": 2.8616199493408203
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.866665840148926,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    },
    {
      "nix_stats": {
        "cpu_time": 2.014240026473999,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 2.014240026473999,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 8216576,
            "vms": 51441664,
            "uss": 5931008,
            "pss": 7124992,
            "swap": 0
          },
          "time": 0.8480744361877441
        },
        {
          "cpu": {
            "user": 0.72,
            "system": 0.18,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 6960,
            "write_count": 7325,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20892977,
            "write_chars": 11655672
          },
          "memory": {
            "rss": 648953856,
            "vms": 711041024,
            "uss": 643182592,
            "pss": 645825536,
            "swap": 0
          },
          "time": 1.8528037071228027
        },
        {
          "cpu": {
            "user": 1.41,
            "system": 0.35,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 12907,
            "write_count": 17266,
            "read_bytes": 33249794,
            "write_bytes": 0,
            "read_chars": 39976105,
            "write_chars": 28503391
          },
          "memory": {
            "rss": 1318993920,
            "vms": 1396408320,
            "uss": 1313017856,
            "pss": 1315660800,
            "swap": 0
          },
          "time": 2.8598434925079346
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.865846633911133,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    },
    {
      "nix_stats": {
        "cpu_time": 1.983597993850708,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 1.983597993850708,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 7909376,
            "vms": 51441664,
            "uss": 6119424,
            "pss": 7292928,
            "swap": 0
          },
          "time": 0.8472259044647217
        },
        {
          "cpu": {
            "user": 0.72,
            "system": 0.18,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 6960,
            "write_count": 7325,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20891549,
            "write_chars": 11651893
          },
          "memory": {
            "rss": 649322496,
            "vms": 727818240,
            "uss": 643174400,
            "pss": 645794816,
            "swap": 0
          },
          "time": 1.8517541885375977
        },
        {
          "cpu": {
            "user": 1.41,
            "system": 0.37,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 12841,
            "write_count": 17221,
            "read_bytes": 33258862,
            "write_bytes": 0,
            "read_chars": 40003924,
            "write_chars": 28594207
          },
          "memory": {
            "rss": 1322246144,
            "vms": 1396670464,
            "uss": 1314426880,
            "pss": 1317047296,
            "swap": 0
          },
          "time": 2.8587911128997803
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.863799810409546,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    },
    {
      "nix_stats": {
        "cpu_time": 2.002357006072998,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 2.002357006072998,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 8290304,
            "vms": 51441664,
            "uss": 6062080,
            "pss": 7245824,
            "swap": 0
          },
          "time": 0.8533148765563965
        },
        {
          "cpu": {
            "user": 0.72,
            "system": 0.17,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 6939,
            "write_count": 7262,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20857460,
            "write_chars": 11493302
          },
          "memory": {
            "rss": 649654272,
            "vms": 710778880,
            "uss": 643928064,
            "pss": 646554624,
            "swap": 0
          },
          "time": 1.8582127094268799
        },
        {
          "cpu": {
            "user": 1.43,
            "system": 0.34,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 12871,
            "write_count": 17148,
            "read_bytes": 33249794,
            "write_bytes": 0,
            "read_chars": 39910987,
            "write_chars": 28200795
          },
          "memory": {
            "rss": 1320218624,
            "vms": 1396146176,
            "uss": 1312559104,
            "pss": 1315185664,
            "swap": 0
          },
          "time": 2.8682892322540283
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.8742563724517822,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    },
    {
      "nix_stats": {
        "cpu_time": 2.01259708404541,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 2.01259708404541,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 8519680,
            "vms": 51441664,
            "uss": 6397952,
            "pss": 7583744,
            "swap": 0
          },
          "time": 0.8552665710449219
        },
        {
          "cpu": {
            "user": 0.73,
            "system": 0.16,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 6916,
            "write_count": 7237,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20855505,
            "write_chars": 11486699
          },
          "memory": {
            "rss": 647471104,
            "vms": 710774784,
            "uss": 641744896,
            "pss": 644381696,
            "swap": 0
          },
          "time": 1.8608319759368896
        },
        {
          "cpu": {
            "user": 1.41,
            "system": 0.34,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 12703,
            "write_count": 16949,
            "read_bytes": 33249794,
            "write_bytes": 0,
            "read_chars": 39886884,
            "write_chars": 28089934
          },
          "memory": {
            "rss": 1314889728,
            "vms": 1395879936,
            "uss": 1309298688,
            "pss": 1311935488,
            "swap": 0
          },
          "time": 2.868189573287964
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.873202085494995,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    },
    {
      "nix_stats": {
        "cpu_time": 1.9842290878295898,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 1.9842290878295898,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 7929856,
            "vms": 51441664,
            "uss": 6184960,
            "pss": 7337984,
            "swap": 0
          },
          "time": 0.8533303737640381
        },
        {
          "cpu": {
            "user": 0.72,
            "system": 0.18,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 6959,
            "write_count": 7319,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20887462,
            "write_chars": 11631824
          },
          "memory": {
            "rss": 649428992,
            "vms": 711041024,
            "uss": 642981888,
            "pss": 645598208,
            "swap": 0
          },
          "time": 1.8581876754760742
        },
        {
          "cpu": {
            "user": 1.4,
            "system": 0.37,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 12931,
            "write_count": 17311,
            "read_bytes": 33258862,
            "write_bytes": 0,
            "read_chars": 40003916,
            "write_chars": 28594297
          },
          "memory": {
            "rss": 1322352640,
            "vms": 1396670464,
            "uss": 1315663872,
            "pss": 1318280192,
            "swap": 0
          },
          "time": 2.865200996398926
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.870542287826538,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    },
    {
      "nix_stats": {
        "cpu_time": 1.9850990772247314,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 1.9850990772247314,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 8142848,
            "vms": 51441664,
            "uss": 6041600,
            "pss": 7196672,
            "swap": 0
          },
          "time": 0.8490707874298096
        },
        {
          "cpu": {
            "user": 0.72,
            "system": 0.17,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 7104,
            "write_count": 7436,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20863963,
            "write_chars": 11522459
          },
          "memory": {
            "rss": 648347648,
            "vms": 711045120,
            "uss": 642203648,
            "pss": 644819968,
            "swap": 0
          },
          "time": 1.8539392948150635
        },
        {
          "cpu": {
            "user": 1.41,
            "system": 0.35,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 13112,
            "write_count": 17473,
            "read_bytes": 33249794,
            "write_bytes": 0,
            "read_chars": 39978507,
            "write_chars": 28517510
          },
          "memory": {
            "rss": 1318912000,
            "vms": 1396408320,
            "uss": 1313034240,
            "pss": 1315650560,
            "swap": 0
          },
          "time": 2.8608148097991943
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.866100311279297,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    },
    {
      "nix_stats": {
        "cpu_time": 1.9612619876861572,
        "envs": {
          "bytes": 147284032,
          "elements": 10772297,
          "number": 7638207
        },
        "gc": {
          "cycles": 0,
          "heap_size": 1526988800,
          "total_bytes": 1516757920
        },
        "list": {
          "bytes": 20914368,
          "concats": 390624,
          "elements": 2614296
        },
        "nr_avoided": 8090858,
        "nr_exprs": 1469182,
        "nr_function_calls": 6649159,
        "nr_lookups": 3978975,
        "nr_op_update_values_copied": 31774690,
        "nr_op_updates": 607131,
        "nr_prim_op_calls": 3261149,
        "nr_thunks": 11004466,
        "sets": {
          "bytes": 679170688,
          "elements": 40539768,
          "number": 1908400
        },
        "sizes": {
          "Attr": 16,
          "Bindings": 16,
          "Env": 8,
          "Value": 24
        },
        "symbols": {
          "bytes": 1016494,
          "number": 85193
        },
        "time": {
          "cpu": 1.9612619876861572,
          "gc": 0.0,
          "gc_fraction": 0.0
        },
        "values": {
          "bytes": 412291368,
          "number": 17178807
        }
      },
      "process_stats": [
        {
          "cpu": {
            "user": 0.0,
            "system": 0.0,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 77,
            "write_count": 0,
            "read_bytes": 61555,
            "write_bytes": 0,
            "read_chars": 61555,
            "write_chars": 0
          },
          "memory": {
            "rss": 8097792,
            "vms": 51441664,
            "uss": 6131712,
            "pss": 7319552,
            "swap": 0
          },
          "time": 0.8472702503204346
        },
        {
          "cpu": {
            "user": 0.7,
            "system": 0.19,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 6940,
            "write_count": 7275,
            "read_bytes": 18074933,
            "write_bytes": 0,
            "read_chars": 20867224,
            "write_chars": 11535834
          },
          "memory": {
            "rss": 648597504,
            "vms": 711036928,
            "uss": 642363392,
            "pss": 645000192,
            "swap": 0
          },
          "time": 1.8520891666412354
        },
        {
          "cpu": {
            "user": 1.4,
            "system": 0.37,
            "children_user": 0.0,
            "children_system": 0.0,
            "iowait": 0.0
          },
          "io": {
            "read_count": 12931,
            "write_count": 17308,
            "read_bytes": 33250758,
            "write_bytes": 0,
            "read_chars": 39992246,
            "write_chars": 28580034
          },
          "memory": {
            "rss": 1320996864,
            "vms": 1396404224,
            "uss": 1313566720,
            "pss": 1316203520,
            "swap": 0
          },
          "time": 2.858891010284424
        }
      ],
      "stderr": "b\"trace: Obsolete option `hardware.opengl.extraPackages' is used. It was renamed to `hardware.graphics.extraPackages'.\\ntrace: Obsolete option `hardware.opengl.package' is used. It was renamed to `hardware.graphics.package'.\\nwarning: failed to perform a full GC before reporting stats\\n\"",
      "wall_time": 3.864964485168457,
      "value": "/nix/store/ja494mjlqc91kglyjyvnnsxlh5h4980k-nixos-system-nixos-desktop-24.11.20241014.a3c0b3b"
    }
  ],
  "description": {
    "gc": {
      "cycles": {
        "min": 0.0,
        "max": 0.0,
        "mean": 0.0,
        "median": 0.0,
        "variance": 0.0,
        "std_dev": 0.0
      },
      "heap_size": {
        "min": 1526988800.0,
        "max": 1526988800.0,
        "mean": 1526988800.0,
        "median": 1526988800.0,
        "variance": 0.0,
        "std_dev": 0.0
      },
      "total_bytes": {
        "min": 1516757920.0,
        "max": 1516757920.0,
        "mean": 1516757920.0,
        "median": 1516757920.0,
        "variance": 0.0,
        "std_dev": 0.0
      }
    },
    "time": {
      "cpu": {
        "min": 1.9612619876861572,
        "max": 2.014240026473999,
        "mean": 1.9902139008045197,
        "median": 1.9846640825271606,
        "variance": 0.0003301331046979986,
        "std_dev": 0.0181695653414714
      },
      "gc": {
        "min": 0.0,
        "max": 0.0,
        "mean": 0.0,
        "median": 0.0,
        "variance": 0.0,
        "std_dev": 0.0
      },
      "gc_fraction": {
        "min": 0.0,
        "max": 0.0,
        "mean": 0.0,
        "median": 0.0,
        "variance": 0.0,
        "std_dev": 0.0
      }
    },
    "wall_time": {
      "min": 3.863799810409546,
      "max": 3.8742563724517822,
      "mean": 3.8681722283363342,
      "median": 3.8663830757141113,
      "variance": 0.000015615934927382114,
      "std_dev": 0.003951700257785516
    }
  }
}
```

</details>
