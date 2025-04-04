# Automata Backend Exercise
## Rock, Paper, Scissors, Lizard, Spock

## Overview
This is a modern take on the classic "Rock, Paper, Scissors" game, with two additional choices: **Lizard** and **Spock**.
The extended rules create more possible outcomes, adding depth and strategy to the game.

## Purpose
The purpose of this exercise is to provide you the opportunity to demonstrate how you solve problems and express code. We are looking for a pragmatic solution that demonstrates your ability to write clean, maintainable, and scalable code. The solution should be a CLI application written in Python

We know that in person code exercises are highly pressured and artificial, hence why we asked you to perform this exercise at home. The expectation is that you will use the tools you are comfortable with (stackoverflow, chatgpt, etc), but you are able to explain and extend the code (as if this was your job). We don't expect you to be able to remember every method of every class, but we would like to have a conversation regarding your code.
## Time limits
Please take no longer than 2-3 hours. The purpose of the exercise is to demonstrate solving a problem in a pragmatic way. We don't
expect a perfect implementation.

## Basic Rules
[The game](https://www.youtube.com/watch?v=pIpmITBocfM) is played between two players. Each player chooses one of the five options:
- **Rock**
- **Paper**
- **Scissors**
- **Lizard**
- **Spock**

The winner is determined by the following rules:

| **Choice**   | **Wins Against** | **Reason**                       |
|--------------|------------------|----------------------------------|
| **Scissors** | Paper, Lizard    | Cuts Paper, Decapitates Lizard   |
| **Paper**    | Rock, Spock      | Covers Rock, Disproves Spock     |
| **Rock**     | Scissors, Lizard | Crushes Scissors, Crushes Lizard |
| **Lizard**   | Paper, Spock     | Eats Paper, Poisons Spock        |
| **Spock**    | Scissors, Rock   | Smashes Scissors, Vaporizes Rock |

If both players choose the same option, the game results in a **tie**.

## Features
- **Interactive Gameplay**: Players can select their choice, and the winner is determined based on the rules.
- **Clear Visual Feedback**: Winning and losing outcomes are displayed in an engaging and intuitive way.
- **Scoreboard**: Tracks the points of the user and the computer across multiple rounds.
- **Data Persistence**: Retains the game state and scoreboard.
- **Restart**: Allows the user to restart the game, clearing the scoreboard and resetting the game state.

## Suggestions
When working on this project, we encourage you to treat the code as if it is intended for a real production environment. Here are some tips to guide you:

- **Code Quality**: Write clean, readable, and maintainable code.
- **Scalability**: Structure your code to allow for easy feature additions or modifications in the future.
- **Version Control**: Use meaningful commit messages that explain the purpose of each change.

## Submitting your code entry
Please provide us with the url to a public github repository.
