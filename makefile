all: circuit edge vertex driver collapse d-algorithm

circuit: Circuit.py
	python -u Circuit.py

edge: Edge.py
	python -u Edge.py

vertex: Vertex.py
	python -u Vertex.py

driver: Driver.py
	python -u Driver.py

collapse: collapse.py
	python -u collapse.py

d-algorithm: d-algo.py
	python -u d-algo.py