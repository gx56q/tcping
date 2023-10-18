<h1 align="center">Welcome to tcping 👋</h1>
<p>
  <a href="https://github.com/gx56q/CloudBackup/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT license" src="https://img.shields.io/badge/License-MIT license-yellow.svg" />
  </a>
</p>

> Utility for TCP ping

## Installation
To use tcping, follow these steps:

#### 1. Clone the repository:
```sh
git clone https://github.com/gx56q/tcping.git
```
#### 2. Navigate to the project directory:
```sh
cd tcping
```
#### 3. Install the required dependencies using pip:
```sh
pip install -r requirements.txt
```

## Usage

The tcping utility provides a simple command-line interface to ping a target host over TCP. The general format of the command is as follows:

```sh
python3 main.py <host> [options]
```

### Target Host
- `host`: The name or IP address of the target host to check.

### Options
These are the optional arguments to customize the behavior of the tcping utility:

| Option                | Description                                                           |
|-----------------------|-----------------------------------------------------------------------|
| `-p` or `--port`      | TCP port number. Default is 80.                                       |
| `-c` or `--count`     | Number of pings to send. If not specified, it continues indefinitely. |
| `-t` or `--timeout`   | Time to wait for a response, in seconds. Default is 1 second.         |
| `-i` or `--interval`  | Interval between pings, in seconds. Default is 1 second.              |


### Examples

#### Basic TCP ping

To check the accessibility of `www.google.com` on port `80`:

```sh
python3 main.py www.google.com
```

#### Specifying Port

To check the accessibility of `www.google.com` on port `443`:

```sh
python3 main.py www.google.com -p 443
```

#### Sending Limited Pings

To send exactly `5` pings to www.google.com:

```sh
python3 main.py www.google.com -c 5
```

#### Setting Timeout

To wait `2` seconds for a response from www.google.com:

```sh
python3 main.py www.google.com -t 2
```

#### Adjusting Interval

To set an interval of `0.5` seconds between pings to www.google.com:

```sh
python3 main.py www.google.com -i 0.5
```

### Help

To get help on the available options, use the `-h` or `--help` option. The command format is:

```sh
python3 main.py --help
```

## Author

👤 **Voinov Andrey**

* Github: [@gx56q](https://github.com/gx56q)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/gx56q/CloudBackup/issues). 

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2023 [Voinov Andrey](https://github.com/gx56q).<br />
This project is [MIT license](https://github.com/gx56q/CloudBackup/blob/master/LICENSE) licensed.

***