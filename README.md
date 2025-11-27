# 🛡️ Network Sentinel - Agentic Monitoring

> **Prototype d'agent autonome pour la supervision d'incidents réseaux.**
> Ce projet démontre l'utilisation de Python pour la détection d'anomalies en temps réel et l'orchestration de réponses via N8N.

## 📋 Contexte du projet
Dans le cadre de la modernisation des infrastructures télécoms (NOC), la détection passive ne suffit plus. Ce projet vise à créer un **Agent Sentinel** capable de :
1. **Monitorer** des flux de logs en temps réel.
2. **Identifier** des patterns critiques (ex: `CORE_SWITCH_FAILURE`).
3. **Déclencher** proactivement un workflow de résolution via Webhook.

## 🛠️ Architecture Technique

```mermaid
graph LR
    A[Server Logs] -->|Monitoring TR| B(Python Sentinel Agent)
    B -->|Détection CRITICAL| C{Decision Engine}
    C -->|Normal| D[Log Archive]
    C -->|Incident| E[Webhook N8N]
    E -->|Alert| F[Microsoft Teams / Slack]
    E -->|Action| G[Ticket Jira Auto]
