# dhandler - Directory handling assistant

## SYNOPSIS

    python dhandler.py [-h] [--func FUNC]
                       --dfrom DFROM --dto DTO [--nopause]

## DESCRIPTION

    dhandler provides methods that can facilitate directory handling.
    Currently available methods include:
        - deploy_dir
        - deploy_empty_subdirs

## OPTIONS

    -h, --help
        Help message

    --func FUNC
        deploy_dir (default)
            Deploy dfrom, including its contents, to dto.
        deploy_empty_subdirs
            Deploy subdirectories of dfrom, excluding their contents, to dto.

    --dfrom DFROM
        The directory from which information will be retrieved

    --dto DTO
        The directory to which the retrieved information will be applied

    --nopause
        Do not pause the shell at the end of the program.

## EXAMPLES

    --func adj_leading_spaces
        python dhandler.py --func deploy_dir --dfrom ./samples/sample3 --dto ./samples/sample3_deployed

    --func adj_leading_spaces
        python dhandler.py --func deploy_empty_subdirs --dfrom ./samples --dto ./samples/samples_unloaded

## REQUIREMENTS

Python 3

## SEE ALSO

[fhandler - File handling assistant](https://github.com/jangcom/fhandler)

## AUTHOR

Jaewoong Jang <<jangj@korea.ac.kr>>

## COPYRIGHT

Copyright (c) 2020 Jaewoong Jang

## LICENSE

This software is available under the MIT license;
the license information is found in "LICENSE".
