# API Reference GhostNet

Ce document détaille l'API REST de GhostNet, qui permet d'interagir programmatiquement avec le système pour gérer les leurres, récupérer les alertes et contrôler diverses fonctionnalités.

## Base URL

```
https://<host>:<port>/api
```

## Authentification

L'API GhostNet utilise l'authentification par token JWT. Pour obtenir un token, envoyez une requête POST à l'endpoint `/auth/login` avec vos identifiants.

```bash
curl -X POST https://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

Réponse :

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2025-04-15T16:00:00Z"
}
```

Pour les requêtes suivantes, incluez le token dans l'en-tête `Authorization` :

```bash
curl -X GET https://localhost:8080/api/status \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Points d'entrée

### Statut

#### GET /api/status

Récupère le statut du système GhostNet.

**Réponse :**

```json
{
  "status": "online",
  "version": "1.0.0",
  "uptime": "10d 4h 30m",
  "modules": {
    "detection": true,
    "lure_generator": true,
    "ai_engine": true
  },
  "timestamp": "2025-04-14T16:30:00Z"
}
```

### Leurres

#### GET /api/lures

Récupère la liste des leurres actifs.

**Paramètres de requête :**

- `page` (optionnel) : Numéro de page pour la pagination (défaut: 1)
- `per_page` (optionnel) : Nombre d'éléments par page (défaut: 10, max: 100)
- `type` (optionnel) : Filtre par type de leurre (ex: "service", "file", "user")
- `status` (optionnel) : Filtre par statut (ex: "active", "inactive")

**Réponse :**

```json
{
  "lures": [
    {
      "id": "lure-001",
      "name": "SSH Server",
      "status": "active",
      "type": "service",
      "service": "ssh",
      "port": 22,
      "created_at": "2025-04-14T10:00:00Z"
    },
    {
      "id": "lure-002",
      "name": "Web Server",
      "status": "active",
      "type": "service",
      "service": "http",
      "port": 80,
      "created_at": "2025-04-14T10:05:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "pages": 1
}
```

#### POST /api/lures

Crée un nouveau leurre.

**Corps de la requête :**

```json
{
  "name": "Database Server",
  "type": "service",
  "service": "mysql",
  "port": 3306,
  "template": "mysql_server",
  "configuration": {
    "version": "5.7",
    "banner": "MySQL 5.7.33",
    "credentials": [
      {"username": "root", "password": "password123"},
      {"username": "dbuser", "password": "userpass"}
    ],
    "databases": [
      {
        "name": "customers",
        "tables": ["users", "orders", "products"]
      }
    ]
  }
}
```

**Réponse :**

```json
{
  "id": "lure-003",
  "name": "Database Server",
  "status": "active",
  "type": "service",
  "service": "mysql",
  "port": 3306,
  "created_at": "2025-04-14T16:45:00Z"
}
```

#### GET /api/lures/{lure_id}

Récupère les détails d'un leurre spécifique.

**Réponse :**

```json
{
  "id": "lure-001",
  "name": "SSH Server",
  "status": "active",
  "type": "service",
  "service": "ssh",
  "port": 22,
  "created_at": "2025-04-14T10:00:00Z",
  "stats": {
    "connections": 15,
    "last_connection": "2025-04-14T15:30:00Z",
    "unique_ips": 3
  },
  "configuration": {
    "banner": "OpenSSH 8.2p1 Ubuntu",
    "credentials": [
      {"username": "root", "password": "password123"},
      {"username": "admin", "password": "admin123"}
    ]
  }
}
```

#### PUT /api/lures/{lure_id}

Met à jour un leurre existant.

**Corps de la requête :**

```json
{
  "name": "SSH Server Updated",
  "status": "inactive",
  "configuration": {
    "banner": "OpenSSH 8.4p1 Debian"
  }
}
```

**Réponse :**

```json
{
  "id": "lure-001",
  "name": "SSH Server Updated",
  "status": "inactive",
  "type": "service",
  "service": "ssh",
  "port": 22,
  "created_at": "2025-04-14T10:00:00Z",
  "updated_at": "2025-04-14T17:00:00Z"
}
```

#### DELETE /api/lures/{lure_id}

Supprime un leurre.

**Réponse :**

```json
{
  "message": "Lure lure-001 deleted successfully"
}
```

### Alertes

#### GET /api/alerts

Récupère la liste des alertes de sécurité.

**Paramètres de requête :**

- `page` (optionnel) : Numéro de page pour la pagination (défaut: 1)
- `per_page` (optionnel) : Nombre d'éléments par page (défaut: 10, max: 100)
- `severity` (optionnel) : Filtre par sévérité (ex: "low", "medium", "high", "critical")
- `type` (optionnel) : Filtre par type d'alerte (ex: "intrusion", "scan", "bruteforce")
- `from` (optionnel) : Filtre par date de début (format ISO 8601)
- `to` (optionnel) : Filtre par date de fin (format ISO 8601)

**Réponse :**

```json
{
  "alerts": [
    {
      "id": "alert-001",
      "timestamp": "2025-04-14T12:00:00Z",
      "severity": "high",
      "source_ip": "192.168.1.100",
      "type": "ssh_bruteforce",
      "description": "Tentative de force brute SSH détectée",
      "details": {
        "attempts": 15,
        "username": "root",
        "duration": 120,
        "lure_id": "lure-001"
      }
    }
  ],
  "total": 1,
  "page": 1,
  "pages": 1
}
```

#### GET /api/alerts/{alert_id}

Récupère les détails d'une alerte spécifique.

**Réponse :**

```json
{
  "id": "alert-001",
  "timestamp": "2025-04-14T12:00:00Z",
  "severity": "high",
  "source_ip": "192.168.1.100",
  "type": "ssh_bruteforce",
  "description": "Tentative de force brute SSH détectée",
  "details": {
    "attempts": 15,
    "username": "root",
    "duration": 120,
    "lure_id": "lure-001"
  },
  "session": {
    "id": "session-001",
    "start_time": "2025-04-14T11:58:00Z",
    "end_time": "2025-04-14T12:01:00Z",
    "commands": [
      {
        "timestamp": "2025-04-14T11:58:30Z",
        "command": "ls -la",
        "output": "total 20\ndrwxr-xr-x 2 root root 4096 Apr 14 10:00 .\ndrwxr-xr-x 6 root root 4096 Apr 14 10:00 .."
      },
      {
        "timestamp": "2025-04-14T11:59:00Z",
        "command": "cat /etc/passwd",
        "output": "root:x:0:0:root:/root:/bin/bash\n..."
      }
    ]
  },
  "attacker_info": {
    "ip": "192.168.1.100",
    "geolocation": {
      "country": "Unknown",
      "city": "Unknown",
      "coordinates": [0, 0]
    },
    "first_seen": "2025-04-14T11:58:00Z",
    "attack_count": 1
  }
}
```

### Attaquants

#### GET /api/attackers

Récupère la liste des attaquants détectés.

**Paramètres de requête :**

- `page` (optionnel) : Numéro de page pour la pagination (défaut: 1)
- `per_page` (optionnel) : Nombre d'éléments par page (défaut: 10, max: 100)
- `severity` (optionnel) : Filtre par niveau de menace (ex: "low", "medium", "high", "critical")

**Réponse :**

```json
{
  "attackers": [
    {
      "ip": "192.168.1.100",
      "first_seen": "2025-04-14T11:58:00Z",
      "last_seen": "2025-04-14T15:30:00Z",
      "attacks": 15,
      "types": ["ssh_bruteforce", "port_scan"],
      "severity": "high",
      "geo": {
        "country": "Unknown",
        "city": "Unknown",
        "coordinates": [0, 0]
      }
    }
  ],
  "total": 1,
  "page": 1,
  "pages": 1
}
```

#### GET /api/attackers/{ip}

Récupère les détails d'un attaquant spécifique.

**Réponse :**

```json
{
  "ip": "192.168.1.100",
  "first_seen": "2025-04-14T11:58:00Z",
  "last_seen": "2025-04-14T15:30:00Z",
  "attacks": 15,
  "types": ["ssh_bruteforce", "port_scan"],
  "severity": "high",
  "geo": {
    "country": "Unknown",
    "city": "Unknown",
    "coordinates": [0, 0]
  },
  "alerts": [
    {
      "id": "alert-001",
      "timestamp": "2025-04-14T12:00:00Z",
      "type": "ssh_bruteforce",
      "lure_id": "lure-001"
    },
    {
      "id": "alert-002",
      "timestamp": "2025-04-14T14:30:00Z",
      "type": "port_scan",
      "lure_id": "lure-002"
    }
  ],
  "sessions": [
    {
      "id": "session-001",
      "start_time": "2025-04-14T11:58:00Z",
      "end_time": "2025-04-14T12:01:00Z",
      "lure_id": "lure-001"
    }
  ],
  "techniques": [
    {
      "name": "T1110.001",
      "description": "Brute Force",
      "confidence": 0.95
    },
    {
      "name": "T1046",
      "description": "Network Service Discovery",
      "confidence": 0.85
    }
  ]
}
```

### Configuration

#### GET /api/config

Récupère la configuration actuelle du système.

**Réponse :**

```json
{
  "general": {
    "name": "GhostNet",
    "version": "1.0.0",
    "log_level": "INFO",
    "api_port": 8080,
    "api_host": "0.0.0.0",
    "enable_ssl": true
  },
  "detection": {
    "enabled": true,
    "modes": ["signature", "anomaly", "behavioral"],
    "sensitivity": 0.8
  },
  "lure_generator": {
    "enabled": true,
    "auto_update": true,
    "mimicry_level": "high"
  },
  "network_manager": {
    "interfaces": [
      {
        "name": "eth0",
        "role": "management"
      },
      {
        "name": "eth1",
        "role": "honeypot"
      }
    ]
  },
  "ai_engine": {
    "enabled": true,
    "mode": "learning"
  },
  "reporting": {
    "alerts": {
      "enabled": true,
      "methods": [
        {
          "type": "email",
          "recipients": ["admin@example.com"],
          "severity_threshold": "high"
        }
      ]
    }
  }
}
```

#### PUT /api/config

Met à jour la configuration du système.

**Corps de la requête :**

```json
{
  "detection": {
    "sensitivity": 0.9,
    "modes": ["signature", "anomaly"]
  },
  "lure_generator": {
    "mimicry_level": "medium"
  }
}
```

**Réponse :**

```json
{
  "message": "Configuration updated successfully",
  "updated_fields": ["detection.sensitivity", "detection.modes", "lure_generator.mimicry_level"]
}
```

### Rapports

#### GET /api/reports

Récupère la liste des rapports disponibles.

**Réponse :**

```json
{
  "reports": [
    {
      "id": "report-001",
      "name": "Rapport journalier - 2025-04-13",
      "type": "daily",
      "format": "pdf",
      "created_at": "2025-04-14T00:00:00Z",
      "url": "/api/reports/report-001/download"
    }
  ],
  "total": 1
}
```

#### POST /api/reports

Génère un nouveau rapport.

**Corps de la requête :**

```json
{
  "type": "custom",
  "period": "2025-04-01T00:00:00Z/2025-04-14T00:00:00Z",
  "format": "pdf",
  "sections": ["summary", "top_attacks", "attacker_analysis", "recommendations"]
}
```

**Réponse :**

```json
{
  "id": "report-002",
  "name": "Rapport personnalisé - Avril 2025",
  "type": "custom",
  "period": "2025-04-01T00:00:00Z/2025-04-14T00:00:00Z",
  "format": "pdf",
  "created_at": "2025-04-14T17:15:00Z",
  "status": "generating",
  "estimated_completion": "2025-04-14T17:20:00Z"
}
```

#### GET /api/reports/{report_id}

Récupère les détails d'un rapport spécifique.

**Réponse :**

```json
{
  "id": "report-001",
  "name": "Rapport journalier - 2025-04-13",
  "type": "daily",
  "format": "pdf",
  "created_at": "2025-04-14T00:00:00Z",
  "size": 1250000,
  "pages": 15,
  "sections": ["summary", "attacks", "attackers", "lures", "recommendations"],
  "highlights": {
    "total_attacks": 25,
    "critical_alerts": 3,
    "unique_attackers": 8,
    "top_attack_type": "ssh_bruteforce"
  },
  "url": "/api/reports/report-001/download"
}
```

#### GET /api/reports/{report_id}/download

Télécharge un rapport spécifique.

**Réponse :**

Le fichier du rapport dans le format demandé (PDF, CSV, etc.).

### Statistiques

#### GET /api/stats

Récupère les statistiques globales du système.

**Paramètres de requête :**

- `period` (optionnel) : Période des statistiques (ex: "day", "week", "month", défaut: "day")
- `from` (optionnel) : Date de début (format ISO 8601)
- `to` (optionnel) : Date de fin (format ISO 8601)

**Réponse :**

```json
{
  "period": "day",
  "start": "2025-04-14T00:00:00Z",
  "end": "2025-04-14T23:59:59Z",
  "alerts": {
    "total": 45,
    "by_severity": {
      "low": 20,
      "medium": 15,
      "high": 8,
      "critical": 2
    },
    "by_type": {
      "ssh_bruteforce": 15,
      "port_scan": 12,
      "web_attack": 10,
      "credential_stuffing": 8
    }
  },
  "attackers": {
    "total": 12,
    "unique_ips": 10,
    "by_country": {
      "Unknown": 8,
      "US": 2,
      "CN": 2
    }
  },
  "lures": {
    "total_active": 5,
    "most_targeted": "lure-001",
    "connections": 78
  },
  "performance": {
    "cpu_usage": 35,
    "memory_usage": 42,
    "storage_usage": 28
  }
}
```

## Codes d'erreur

L'API GhostNet utilise les codes d'état HTTP standard et renvoie les informations d'erreur dans le format suivant :

```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid username or password",
    "status": 401
  }
}
```

### Codes d'erreur courants

| Code d'erreur | Code HTTP | Description |
|---------------|-----------|-------------|
| `UNAUTHORIZED` | 401 | Authentification requise ou token invalide |
| `INVALID_CREDENTIALS` | 401 | Identifiants incorrects |
| `ACCESS_DENIED` | 403 | Autorisation insuffisante pour accéder à la ressource |
| `NOT_FOUND` | 404 | Ressource non trouvée |
| `VALIDATION_ERROR` | 400 | Erreur de validation des données |
| `ALREADY_EXISTS` | 409 | La ressource existe déjà |
| `SERVER_ERROR` | 500 | Erreur interne du serveur |

## Exemples d'utilisation

### Créer un nouveau leurre et récupérer ses statistiques

```bash
# Créer un nouveau leurre
curl -X POST https://localhost:8080/api/lures \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "FTP Server",
    "type": "service",
    "service": "ftp",
    "port": 21,
    "template": "default_ftp_server",
    "configuration": {
      "banner": "FTP server ready",
      "credentials": [
        {"username": "anonymous", "password": ""}
      ]
    }
  }'

# Récupérer les détails du leurre créé (avec l'ID retourné)
curl -X GET https://localhost:8080/api/lures/lure-004 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Récupérer les alertes critiques des dernières 24 heures

```bash
curl -X GET "https://localhost:8080/api/alerts?severity=critical&from=2025-04-13T16:00:00Z&to=2025-04-14T16:00:00Z" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Générer un rapport personnalisé

```bash
curl -X POST https://localhost:8080/api/reports \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "type": "custom",
    "period": "2025-04-01T00:00:00Z/2025-04-14T00:00:00Z",
    "format": "pdf",
    "sections": ["summary", "top_attacks", "attacker_analysis", "recommendations"]
  }'
```
