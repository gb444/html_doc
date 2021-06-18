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
    with d.p:
        d.ital("This an i in a p in the div")
```

If we wanted to add a class to that, we can invoke it with arguments (this is possibly rather counterintuitive)

```python
with d.div(classes=['my-class']):
    d.p("This element will be within a div with the my-class class")
```

If we're just adding one nested tag, we can be a bit cheeky:
```python
d.p(d.ital("Italic in a p"))
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

## Tables
Although one can construct tables the old fashioned way with lots of nested elements, this is rather dry and 
requires too much knowledge of html for casual tableage:

```python
d.easy_table([['row 1, col 1', 'row 1, col 2'],
              ['row 2, col 1', 'row 2, col 2']],
             columns=['Column 1', 'Column 2'])

d.easy_table(df) # Pandas dataframes also supported

```

## Figures
Matplotlib figures are easy too:
```python
    import matplotlib.pyplot as plt
    import numpy as np
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    plt.plot(t, s)

    plt.gca().set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    plt.grid()
    d.easy_plot()
    d.easy_plot(render_as='raster') 
    d.easy_plot(plt.gcf(), fix_size=False)
    d.easy_plot(size_inches=(3,2))
    d.easy_plot(size_cm=(10,5))
    

```
By default it renders via svg but this doesn't work 100% of the time (had problems with error bars) 
and can be slow to view for plots with 1000s of lines/points. 