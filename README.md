# shuffle-lunch
Build shuffle-lunch groups.

## 1. Getting Started

Run `main.py` with arguments (selection method and the number of months to simulate):
```bash
python main.py greedy 10
```

### 1.1. Selection Method

Support two types of methods for selection

- greedy: greedy method
- random: random method; randomly build groups 10,000 times and select the best group.

### 1.2. Number of Months for Simulation

Specify the number of months for simulation. For example, if 10 is passed, it will simulate selection for 10 months.

## 2. Scoring System

Basically, higher score is worse.

- 1: Two people in a group had lunch together 3 months ago.
- 2: Two people in a group had lunch together 2 months ago.
- 3: Two people in a group had lunch together 1 month ago.
- 4: Two people in a group are in same team; they probably have lunch together frequently.
