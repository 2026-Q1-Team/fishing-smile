# Introduction

Security awareness is a core pillar of security, it is a skill that needs to be learned and practiced by all members of
an organization in order to ensure operational security.
Fishing-Smile is a tool created for the purpose of providing support in phishing-awareness training as a part of
security awareness training by providing simulated phishing scenarios to test and evaluate the readiness of the
subjects.
In this document the general details regarding the tool and its requirements will be laid out, including the purpose,
scope, and definitions of any acronyms and abbreviations, meant for clarity and ease of information retention.

## Document Purpose

The purpose of this document is to lay out the software requirements of the system in a clear and concise form both for
archival purpose, and as a foundation and guideline for development of the tool hereafter.
This document will cover the description, requirements, and traceability matrix for the system.

## Scope

The fishing-smile system is a tool for phishing-attack awareness training, it can be used to simulate an attack in
and perform evaluation on any subjects specified by the user, with provided dashboard displays for ease of
management.
Additionally, the scheme of each attack can be customized to match any requirements of the user in order to train
subjects to catch specific red-flags that count towards the evaluation metric.
This can allow users to streamline the process of awareness training and improve effectiveness by optionally providing
quick feedback to the subjects instead of a more traditional training method.

## Intended Audience and Document Overview

This document is intended for internal use of the fishing-smile development team. It is separated into six chapters,
introduction, overall description, specific requirements, other non-functional requirements, and requirements
traceability respectively.
It is recommended that the reader skip the introduction and earlier pages of the overall description if one already
understands the basic premise of the product and merely wishes to view the more technical part of this documentation.

## Definitions, Acronyms, and Abbreviations

## References and Acknowledgements

# Overall Description

## System Overview

Fishing-smile is a phishing-attack simulation tool, it is a system designed to perform simulated phishing attacks on any
user-specified targets and provide evaluation of a target's awareness of the ongoing attack scenario simulation.
This tool is developed primarily to provide support for any security awareness training regiment, in order to be used in
tandem with other educational tool and evaluation methods.

```mermaid
placeholder1->placeholder2
```

## System Functionality

There are five main functions that the fishing-smile tool offers.

+ Email content generation based on attack schemes and target profiles.
+ Landing page content generation based on attack schemes. (WIP)
+ Sending emails to target addresses.
+ Tracking and recording target interaction with the system.
+ Summarizing target risk factor as part of a security awareness training program.

## Design and Implementation Constraints

This tool is designed for the personal desktop computer and personal laptop computer.
It is currently not possible to track a target's interaction with the email contents itself, only the website that the
URL that should be present in every email directs to.

## Assumptions and Dependencies

It is assumed that the user has explicit permission to perform any such simulated phishing attacks on all targets
referenced in the simulated attack itself.
This tool is not to be used to perform the simulated phishing attack function without explicit permission from involved
parties.
For this tool to function as intended -- one, the user must ensure that [add dependencies here]

# Specific Requirements

## Business and User Requirements

## Functional Requirements

## Use Case Model

# Other Non-functional Requirements

## Safety and Security Requirements

## Software Quality Attributes

# Traceability Matrix
