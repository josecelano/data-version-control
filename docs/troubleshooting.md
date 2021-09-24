## Troubleshooting

### Activate conda environment using act or github runner

If you try to activate a conda environment, you can get an error like this:

```
[Resize image using conda/resize_with_conda] ⭐  Run Activate environment
[Resize image using conda/resize_with_conda]   🐳  docker exec cmd=[bash --noprofile --norc -e -o pipefail /home/josecelano/Documents/github/josecelano/data-version-control/workflow/2] user=
| 
| CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
| To initialize your shell, run
| 
|     $ conda init <SHELL_NAME>
| 
| Currently supported shells are:
|   - bash
|   - fish
|   - tcsh
|   - xonsh
|   - zsh
|   - powershell
| 
| See 'conda init --help' for more information and options.
| 
| IMPORTANT: You may need to close and restart your shell after running 'conda init'.
| 
| 
[Resize image using conda/resize_with_conda]   ❌  Failure - Activate environment
```

The long explanation is here: https://github.com/marketplace/actions/setup-miniconda#important

You can fix executing this command `bash -l {0}` before any other command in your tasks. You can also add this to your workflow to automatically add it to all your tasks:

```
defaults:
    run:
    shell: bash -l {0}  
```