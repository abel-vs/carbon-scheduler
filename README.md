<div id="top"></div>

  <h3 align="center">The CAS tool</h3>

  <p align="center">
    A Carbon Aware Scheduler for Unix jobs
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>


## About The Carbon Aware Scheduler

The Carbon Aware Scheduler (CAS) is a command line tool that takes CO2 into account when scheduling intensive jobs on the computer. Given a job, this job will find the best time of the day to run a job based on collected data. The data is currently based on some heuristics and it's only related to the Netherlands. The tool is a wrapper around the Cron tool for scheduling unix commands and the at tool. 

This tool can help you:
* Schedule non-urgent jobs at a later time during the day
* Save CO2 and visualize total CO2 saved
* Easily manage your cron jobs

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

This project was built in [Python ](https://www.python.org/)and some of the main dependencies are:

* [python-crontab](https://pypi.org/project/python-crontab/)
* [croniter](https://pypi.org/project/croniter/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

Here are the instructions on getting started with our tool. Whether you want to use this tool to become more environmentally-friendly or simply contribute to a tool that changes the world, you can find the instructions here.



### Installation

If you simply want to use the app and benefit from the carbon aware scheduling, simply execute the step below:

* Install the package with pip
  ```sh
  pip install cas
  ```



### Contributing

In order to contribute to this project, 

1. Clone the repo
   ```sh
   git clone https://github.com/abel-vs/carbon-scheduler
   ```

2. Install the requirements

   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



## Usage

Some useful use cases of this tool can be found below:

1. Scheduling a one-off job
2. Scheduling a repeating job
3. Listing all the scheduled jobs, repeating and one-off jobs
4. Cancelling a repeating job 
5. Cancelling a one-off job

<p align="right">(<a href="#top">back to top</a>)</p>



## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish



See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

Wander - email@example.com

Abel -

Florentin - 

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* Luis Cruz

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/abel-vs/carbon-scheduler/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png