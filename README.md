<p align="center">
    <h1 align="center">MQTT-MSEED2INFLUXDB PROXY</h1>
</p>
<p align="center">
    <em>► Applicazione/Proxy che scrive pacchetti <code>MSEED</code> da MQTT su InfluxDB per la gestione e l'analisi di dati sismici</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/dennisrapaccini/mqtt-mseed2influxdb?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/dennisrapaccini/mqtt-mseed2influxdb?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/dennisrapaccini/mqtt-mseed2influxdb?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/dennisrapaccini/mqtt-mseed2influxdb?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Sviluppato con i seguenti linguaggi e tools</em>:
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/InfluxDB-22ADF6?style=flat&logo=InfluxDB&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/grafana-%23F46800.svg?style=flat&logo=grafana&logoColor=white" alt="Docker">
</p>
<hr>

##  Links

> - [Sommario](#sommario)
> - [Features](#features)
> - [Struttura del progetto](#struttura-del-progetto)
> - [Modules](#modules)
> - [Come iniziare](#come-iniziare)
>   - [ Installazione manuale](#installazione-manuale)
>   - [ Installazione mediante Docker](#-nstallazione-mediante-docker)
>   - [ Running mqtt-mseed2influxdb](#-running-mqtt-mseed2influxdb)
>   - [ Tests](#-tests)
> - [ Project Roadmap](#-project-roadmap)
> - [ Contributing](#-contributing)
> - [ License](#-license)
> - [ Acknowledgments](#-acknowledgments)

---

## Sommario

<code>► INSERT-TEXT-HERE</code>

---

## Features

<code>► INSERT-TEXT-HERE</code>

---

## Struttura del progetto

```sh
└── mqtt-mseed2influxdb/
    ├── Dockerfile
    ├── config.ini
    ├── datasource.yaml
    ├── docker-compose.yml
    ├── grafana-provisioning
    │   └── datasources
    │       └── datasource.yaml
    ├── requirements.txt
    └── src
        ├── certs
        │   ├── ca.crt
        │   ├── client.crt
        │   └── client.key
        ├── logs
        │   └── errors.log
        └── proxy_unified.py
```

---

## Modules

<details closed><summary>.</summary>

| File                                                                                                        | Summary                         |
| ---                                                                                                         | ---                             |
| [docker-compose.yml](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/docker-compose.yml) | <code>► INSERT-TEXT-HERE</code> |
| [Dockerfile](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/Dockerfile)                 | <code>► INSERT-TEXT-HERE</code> |
| [datasource.yaml](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/datasource.yaml)       | <code>► INSERT-TEXT-HERE</code> |
| [requirements.txt](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/requirements.txt)     | <code>► INSERT-TEXT-HERE</code> |

</details>

<details closed><summary>grafana-provisioning.datasources</summary>

| File                                                                                                                                   | Summary                         |
| ---                                                                                                                                    | ---                             |
| [datasource.yaml](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/grafana-provisioning/datasources/datasource.yaml) | <code>► INSERT-TEXT-HERE</code> |

</details>

<details closed><summary>src</summary>

| File                                                                                                        | Summary                         |
| ---                                                                                                         | ---                             |
| [proxy_unified.py](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/src/proxy_unified.py) | <code>► INSERT-TEXT-HERE</code> |

</details>

<details closed><summary>src.certs</summary>

| File                                                                                                  | Summary                         |
| ---                                                                                                   | ---                             |
| [ca.crt](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/src/certs/ca.crt)         | <code>► INSERT-TEXT-HERE</code> |
| [client.crt](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/master/src/certs/client.crt) | <code>► INSERT-TEXT-HERE</code> |

</details>

---

## Come iniziare
L'installazione può essere eseguita secondo due approcci: manualmente o mediante l'utilizzo di Docker-Compose. Si raccomanda di adottare il secondo per una maggiore semplicità e coerenza nell'ambiente di esecuzione.

> [!NOTE]
> 
> _I passi riportati sono specifici per sistemi Ubuntu/Debian, ma possono essere facilmente estesi ad altri sistemi._

### Prerequisiti
Preliminarmente, è necessario installare le seguenti dipendenze.

Se si procede __manualmente__:

  - Git
  - Python:latest
  - Packages presenti in [requirements.txt](requirements.txt) mediante `pip install`

Se si procede con __docker__:
  - Git
  - Docker e Docker Compose (automaticamente installati con Docker Desktop)

### Installazione manuale
1. Clonare la repository:
   
	```sh
	$ git clone https://github.com/dennisrapaccini/mqtt-mseed2influxdb
	```
2. Scaricare e installare _InfluxDB_:
   
   	```sh
	$ curl -O https://download.influxdata.com/influxdb/releases/influxdb2_2.7.6-1_amd64.deb
    $ sudo dpkg -i influxdb2_2.7.6-1_amd64.deb
	```
    Per altri sistemi, fare riferimento alla [documentazione](https://docs.influxdata.com/influxdb/v2/install/?t=Linux) ufficiale.
> [!NOTE]
>
> _Potrebbe capitare che `curl` non riesca a scaricare correttamente il pacchetto e quindi risulta necessario scaricarlo e installarlo manualmente (es. mediante un gestore pacchetti).\
> Si __sconsiglia fortemente__ di installarlo con `sudo apt-get install influxdb` in quanto la versione non sarebbe compatibile con il presente progetto._

   
3. Scaricare e installare _Grafana_:

   	```sh
	$ wget -q -O - https://packages.grafana.com/gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/grafana.gpg > /dev/null
    $ echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
    $ sudo apt update
    $ sudo apt install grafana
	```
    Analogamente al precedente, per altri sistemi, fare riferimento alla [documentazione](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) ufficiale.

### Installazione mediante Docker (consigliata)
1. Clonare la repository:
   
	```sh
	$ git clone https://github.com/dennisrapaccini/mqtt-mseed2influxdb
	```
 
 2. Comporre i container di _InfluxDB_ e _Grafana_:

	```sh
	$ docker-compose up -d influxdb grafana
	```
## Configurazione
Prima di avviare l'applicazione, è necessario configurare il _broker MQTT_, _InfluxDB_, _Grafana_ e il _proxy_ modificando i file [.env](.env) e [config.ini](config.ini). 

#### Broker MQTT 
Nel file [config.ini](config.ini), sotto le sezioni `[TLS]` e `[MQTT]`, si possono modificare i vari parametri di rete e di protocollo per la comunicazione con i sensori. 
```ini
[TLS]
ca_cert = src/certs/ca.crt
client_cert = src/certs/client.crt
client_key = src/certs/client.key

[MQTT]
broker = 193.205.129.120
port = 8883
qos = 1
topic = S.H.M.
```

#### InfluxDB
Il client InfluxDB può essere settato utilizzando le **variabili d'ambiente** (.env) o utilizzando la **UI**.
- Il file [.env][.env] contiene le variabili d'ambiente necessarie ad InfluxDB per inizializzare un nuovo database e per 



### Uso

Use the following command to run mqtt-mseed2influxdb:

```sh
> INSERT-RUN-COMMANDS
```

### Tests

To execute tests, run:

```sh
> INSERT-TEST-COMMANDS
```

---

## Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

## Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/dennisrapaccini/mqtt-mseed2influxdb/issues)**: Submit bugs found or log feature requests for Mqtt-mseed2influxdb.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/dennisrapaccini/mqtt-mseed2influxdb
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-quick-links)

---
