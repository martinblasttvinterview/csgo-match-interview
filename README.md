# CS:GO Match Visualizer

## Technologies

* **Python 3.12**
* **FastAPI**
* **React**
* **Docker**

## Overview

This project aims to parse, and expose match statistics from a CS:GO tournament match.
These statistics will then be Visualized in a frontend.

### Scope

In order to keep the project simple and within scope, I won’t implement a database. Instead, all events will be loaded directly into memory when the match data is processed. I will also focus on the quality of the code, rather than exposing too many statistics.

## Backend Design

### Focused Stats

To begin with, I will add: **round average length** and **number of kills per player**. After that it would be interesting to display position data of killed players in a heatmap (over time?), and money spent per round. 


### Event Parsing

The CS:GO match log emits many different events, but to keep the scope limited, I will implement only the essential events required for the statistics mentioned above. The backend will need to handle multiple event types and extract relevant data from them.

### Design Principles

I will follow SOLID principles, especially for the event registration system. When adding support for a new event, it should be as easy as creating a new class that implements a base event interface. This class will then be registered with an event registry, which will later be used during the parsing process.
