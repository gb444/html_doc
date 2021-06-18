# Introduction

`html_doc` aims to be an extremely terse way of adding document generation to code.

It was developed with automatic reporting in mind, whether analytic outputs, formatting of 
technical files or just putting together a few matplotlib plots with some numbers. 

It uses some slightly odd technical tricks internally to make the use more consistent, 
those details will be documented elsewhere to prosperity.

It does somewhat require some extremely basic knowledge of HTML to use, but I hope no CSS unless 
more customisation is wanted

It is designed to be very extensible, with the idea that any project that uses it will implement their
own class-based extension that defines custom elements and styling.

## Why not templates?
Some might ask, why not just use jinja2 or handlebars or one of the hundreds of other templating engines there are?

I've found that for complex data structures, I end up writing code that maps 
[real data structure] -> [data structure for template] -> [template], this
library allows much less code and faff for simple documents. For code that is 90%
written for this output itself, there's no point having so much seperation.

I also was after something that was designed to create reasonably pretty documents directly
without having to mess about with CSS most of the time, or even really with HTML - where making a PDF
for non-technical users was *almost* as easy as a `print()`.

# Quick intro

Basic usage is extremely simple:
```python
d = HtmlDoc("Document Title")
d.h1("Heading")
d.p("This is the first paragraph of the document")

d.to_pdf("output.pdf")
```


## Nested tags
As we know, HTML uses nested tags for more or less anything, and html_doc makes this extremely easy:
```python
with d.div:
    d.p("This p is in the div")
    d.p("This p is in the div")
```

If we wanted to add a class to that, we can invoke it with arguments (this is possibly rather counterintuitive)

```python
with d.div(classes=['my-class']):
    d.p("This element will be within a div with the my-class class")
```

If we're just adding one nested tag, we can be a bit cheeky:
```python
d.p(d.ital("Italic in a para"))
```

## Raw HTML

```python
d.raw("<div><p>Some HTML</p></div>")
with d.p:
    d.raw("This will end up being within a p with nothing else")
```

## Images
For simplicity, images are handled using data URIs - this is nice as it allows the HTML documents
created to be completely stand-alone. 

```python
# png
d.img(png=open('tests/example.png', 'rb').read())
d.img(path='tests/example.png')
# jpg
d.img(jpg=open('tests/example.jpg', 'rb').read())
d.img(path='tests/example.jpg')
# svg
d.img(svg=open('tests/example.svg').read())
d.img(path='tests/example.svg')
d.svg(open('tests/example.svg').read())

# width and height
d.img(path='tests/example.svg', width="2in")
d.img(path='tests/example.svg', height="25mm")
```

