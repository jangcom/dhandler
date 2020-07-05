# dhandler

<?xml version="1.0" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<link rev="made" href="mailto:" />
</head>

<body>



<ul id="index">
  <li><a href="#NAME">NAME</a></li>
  <li><a href="#SYNOPSIS">SYNOPSIS</a></li>
  <li><a href="#DESCRIPTION">DESCRIPTION</a></li>
  <li><a href="#OPTIONS">OPTIONS</a></li>
  <li><a href="#EXAMPLES">EXAMPLES</a></li>
  <li><a href="#REQUIREMENTS">REQUIREMENTS</a></li>
  <li><a href="#SEE-ALSO">SEE ALSO</a></li>
  <li><a href="#AUTHOR">AUTHOR</a></li>
  <li><a href="#COPYRIGHT">COPYRIGHT</a></li>
  <li><a href="#LICENSE">LICENSE</a></li>
</ul>

<h1 id="NAME">NAME</h1>

<p>dhandler - Directory handling assistant</p>

<h1 id="SYNOPSIS">SYNOPSIS</h1>

<pre><code>    python dhandler.py [-h] [--func FUNC]
                       --dfrom DFROM --dto DTO [--nopause]</code></pre>

<h1 id="DESCRIPTION">DESCRIPTION</h1>

<pre><code>    dhandler provides functions that can facilitate directory handling.
    Currently available functions include:
        - deploy_dir
        - deploy_empty_subdirs</code></pre>

<h1 id="OPTIONS">OPTIONS</h1>

<pre><code>    -h, --help
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
        Do not pause the shell at the end of the program.</code></pre>

<h1 id="EXAMPLES">EXAMPLES</h1>

<pre><code>    --func adj_leading_spaces
        python dhandler.py --func deploy_dir --dfrom ./samples/sample3 --dto ./samples/sample3_deployed

    --func adj_leading_spaces
        python dhandler.py --func deploy_empty_subdirs --dfrom ./samples --dto ./samples/samples_unloaded</code></pre>

<h1 id="REQUIREMENTS">REQUIREMENTS</h1>

<p>Python 3</p>

<h1 id="SEE-ALSO">SEE ALSO</h1>

<p><a href="https://github.com/jangcom/fhandler">fhandler - File handling assistant</a></p>

<h1 id="AUTHOR">AUTHOR</h1>

<p>Jaewoong Jang &lt;jangj@korea.ac.kr&gt;</p>

<h1 id="COPYRIGHT">COPYRIGHT</h1>

<p>Copyright (c) 2020 Jaewoong Jang</p>

<h1 id="LICENSE">LICENSE</h1>

<p>This software is available under the MIT license; the license information is found in &#39;LICENSE&#39;.</p>


</body>

</html>