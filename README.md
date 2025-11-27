# Network Sentinel - Agentic Incident Response

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![N8N](https://img.shields.io/badge/Orchestration-N8N-red?style=flat&logo=n8n)
![AI](https://img.shields.io/badge/Agentic-AI-green?style=flat)

> **Agent autonome de supervision capable de détecter des anomalies réseaux en temps réel, de diagnostiquer la cause via IA, et d'orchestrer la réponse opérationnelle.**

## Contexte du projet
Dans le cadre de l'évolution vers les réseaux autonomes (Self-Organizing Networks), la simple surveillance passive ne suffit plus. Ce projet, **Network Sentinel**, est un prototype d'ingénierie visant à démontrer comment coupler **l'observabilité classique** (Logs) avec **l'IA Agentique** pour réduire le MTTR (Mean Time To Repair).

**Objectifs :**
1. **Détection** : Monitorer des flux de logs en temps réel.
2. **Décision** : Utiliser un LLM pour analyser l'erreur technique.
3. **Action** : Déclencher proactivement une alerte enrichie avec une solution technique.

---

## Architecture Technique

Le système repose sur une approche découplée : un agent léger en Python pour la collecte et un cerveau déporté sur N8N pour l'intelligence.

```mermaid
graph LR
    A[Server Logs] -->|Tail & Parse| B(Python Sentinel Agent)
    B -->|Détection CRITICAL| C{Decision Engine}
    C -->|Normal| D[Log Archive]
    C -->|Incident| E[Webhook N8N]
    subgraph "N8N Intelligence"
    E -->|Context| F[AI Agent / LLM]
    F -->|Analysis & Fix| G[Slack/Teams Alert]
    end
