# Jenkins Job Killer

Jenkins Job Killer is a Python script designed to manage and terminate Jenkins jobs that are running longer than a specified timeout. This tool can help maintain the health of your Jenkins instance by preventing runaway jobs.

## Features

- Authenticate with Jenkins server
- Display Jenkins server version
- List current queued jobs
- Identify and terminate running jobs that exceed a specified timeout
- Dry run mode for safe testing

## Installation

You can install Jenkins Job Killer by downloading the binary from the releases page (only available for MacOs) and placing it in your `/usr/local/bin` directory.

### Using curl

Run the following command to download and install Jenkins Job Killer:

#### Intel
```sh
curl -L -o jjkiller https://github.com/matandomuertos/jenkins-job-killer/releases/download/latest/jjkiller_intel && chmod +x jjkiller && sudo mv jjkiller /usr/local/bin/jjkiller
```

#### ARM
```sh
curl -L -o jjkiller https://github.com/matandomuertos/jenkins-job-killer/releases/download/latest/jjkiller_amd && chmod +x jjkiller && sudo mv jjkiller /usr/local/bin/jjkiller
```

## Usage

Jenkins Job Killer provides various command-line options to interact with your Jenkins server. Below are some examples of how to use it.

### Basic Command

```sh
jjkiller --url http://your-jenkins-url -u your-username -p your-password
```

### Options

- `-url`, `--url`: Specify the Jenkins server URL (required)
- `-u`, `--user`: Specify the Jenkins username (required)
- `-p`, `--password`: Specify the Jenkins password or token (required)
- `--queue`: Cleans up queued builds
- `--version`: Print the Jenkins server version
- `--time-out`, `-t`: Set the timeout (in hours) for builds that need to be stopped (default: 4 hours)
- `--dry-run`: Run in dry mode, no builds will be stopped

### Examples

#### Print Jenkins Server Version

```sh
jjkiller --url http://your-jenkins-url -u your-username -p your-password --version
```

#### Terminate Queued Jobs And Build Running Over 6 Hours

```sh
jjkiller --url http://your-jenkins-url -u your-username -p your-password --queue
```

#### Terminate Builds Running Over 6 Hours

```sh
jjkiller --url http://your-jenkins-url -u your-username -p your-password --time-out 6
```

#### Dry Run (No Builds Will Be Stopped or cancelled)

```sh
jjkiller --url http://your-jenkins-url -u your-username -p your-password --dry-run
```

## Development

### Requirements

- Python 3.6+
- `jenkins` Python package
- `argparse` Python package
- `tabulate` Python package

### Setup

1. Clone the repository

   ```sh
   git clone https://github.com/matandomuertos/jenkins-job-killer.git
   cd jenkins-job-killer
   ```

2. Install the required packages

   ```sh
   pip install -r requirements.txt
   ```

3. Run the script

   ```sh
   python src/jobKiller.py --url http://your-jenkins-url -u your-username -p your-password
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
