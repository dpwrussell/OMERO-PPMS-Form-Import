var re = {
  inputs: {
    mandatory: /\]\*/,
    text: /^[ ]*\[FT([0-9]*)\][\*]?[ ]*$/,
    date: /^[ ]*\[DT\][\*]?[ ]*$/,
    checkbox: /^\[CB\][\*]?(\$TSEC([0-9]+)\$)?(.+)$/,
    radio: /^\[RD\][\*]?(\$TSEC([0-9]+)\$)?(.+)$/,
    upload: /^[ ]*\[UP\][\*]?[ ]*$/
  },
  section : /\$(\/)?SEC([0-9]+)\$/,
  //The next RegEx can be helpful to retrieve the answer in the content
  title: /^[!]{2}[^!](.)+$/,
  subtitle: /^[!]{3}(.)+$/,
  tags: {
    bold: /\$b\$(.+)\$\/b\$/g,
    image: /\$img\$(.+)\$\/img\$/g,
    url: /\$url\$(.+)\$\/url\$/g,
    pop: /\$pop\$(.+)\$\/pop\$/g
  },
  filled: {
  text: /^\[([^x_].+)\]$/,
  checkbox: /^\[(x|_)\](.+)$/,
  radio: /^\((x|_)\)(.+)$/
  }
};
