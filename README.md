# TEI Processing-Model-Lib

A small and more a less Proof-Of-Concept implementation of the TEI Processing Model in Python and XSLT 3.0.

## Some notes on the idea of this project

The idea of the processing model is to describe to intended output of TEI encoded documents in a declartive fashion by using TEI (see the [Guidelines](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/TD.html#TDTAG) for more details). By now there is only one existing implementation, which can or should be used in production: [the core library of the TEI Publisher](https://github.com/eeditiones/tei-publisher-lib).

This project tries to implement the processing model using python and XSLT and is heavily inspired by the initial work done by [Magdalena Turska](https://github.com/tuurma) in the context of the [TEISimple Project](https://github.com/TEIC/TEI-Simple).

## Keypoints, which will make this implementation different / unique

The core of this implementation are just a few small XSLT-scripts. The only thing needed for running this scripts is an XSLT 3.0 aware processor. The python package is just a wrapper, which should make the usage more convient. In contrast to the TEI Publisher library this means, we're using a more or less completly different tech stack. The implementation of the TEI Publisher is based on eXist-DB and XQuery, which may be sufficient for most of the time. All in all using XQuery for (heavy) transformations-task may not be the best idea. XQuery was and still is foremost a language to query XML. Or in other words: Just because you have a hammer doesn't mean everything is a nail. XSLT, on the other hand, was developed from the ground up for precisely this purpose.

In contrast to the original TEISimple implementation more or less the following points will make this implementation diffent:

- it uses XSLT 3.0 and modern features baked in
- it favours push before pull
- the order of `tei:model` inside an `tei:elementSpec` doesn't matter; instead it relies on the specifity of the `@predicate`-rules as proposed in the [Guidelines in 22.5.4.9](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/TD.html#TDPMIP)
- it makes no assumptions about how the output should look like and therefore does not embed any CSS, JS or anything else

## State of this project

The actual state is just a first quick and dirty proof of concept and does not implement all feature. You should not try to use this production at the moment. The only supported output-mode at the moment is web! Just a few behaviours a implemented by now.

## Dependencies:

- [saxonche](https://pypi.org/project/saxonche/)
- see `pyproject.toml` for all the other dependencies for development


## Author / Contact

- [Bastian Politycki](https://github.com/Bpolitycki) – Swiss Law Sources
