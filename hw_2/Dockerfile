FROM python:3.6
WORKDIR /workdir
COPY medium.py medium.py
COPY easy.py easy.py
COPY fib.py fib.py
RUN mkdir -p /workdir/artifacts
RUN apt-get update
RUN python3 -m pip install pydot networkx astdrawercabpacob pdflatex
RUN apt-get -y install graphviz texlive

CMD python3 /workdir/medium.py
