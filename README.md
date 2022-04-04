<div id="top"></div>

  <h3 align="center">CAS</h3>

  <p align="center">
    A Carbon-aware scheduler for Unix jobs
    <br />
    <a href="https://github.com/abel-vs/carbon-scheduler/issues">Report Bug</a>
    ·
    <a href="https://github.com/abel-vs/carbon-scheduler/issues">Request Feature</a>
    ·
    <a href="https://github.com/abel-vs/carbon-scheduler/pulls">Contribute</a>
  </p>


## About Carbon Aware Scheduler

Carbon Aware Scheduler (CAS) is a command line tool that takes CO2 into account when scheduling jobs. Given a job, this job will find the best time of the day to run a job based on a model of [carbon intensity](https://en.wikipedia.org/wiki/Emission_intensity#Electric_generation) of the power grid. The amount of CO2 emitted per kWh (the aforementioned carbon intensity) often varies greatly during the day, so smart scheduling can reduce CO2 emissions. The model is based on heuristics and it's currently only available for the Netherlands. The tool is a wrapper around the `cron` and `at` tools for scheduling Unix commands.

This tool can help you:
* Schedule non-urgent jobs at a later time during the day
* Save CO2 and visualize total CO2 saved
* Easily manage your `cron` and `at` jobs

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

This project was built in [Python ](https://www.python.org/)and some of the main dependencies are:

* [python-crontab](https://pypi.org/project/python-crontab/)
* [croniter](https://pypi.org/project/croniter/)

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

Here are the instructions on getting started with our tool. Whether you want to use this tool to become more environmentally-friendly or simply contribute to a tool that changes the world, you can find the instructions here.

### Installation

If you simply want to use the app and benefit from the carbon aware-scheduling, simply run:

  ```sh
  pip install carbon-aware-scheduler
  ```



### Contributing

In order to contribute to this project, 

1. Fork the repo using the web interface or using the `gh` CLI:
   ```sh
   gh repo fork https://github.com/abel-vs/carbon-scheduler --clone
   ```

2. Install the requirements

   ```sh
   pip install -r requirements.txt
   ```

3. Make some commits!

4. Open a [Pull Request](https://github.com/abel-vs/carbon-scheduler/pulls)

<p align="right">(<a href="#top">back to top</a>)</p>



<!--## Usage

Some useful use cases of this tool can be found below:

1. Scheduling a one-off job
2. Scheduling a repeating job
3. Listing all the scheduled jobs, repeating and one-off jobs
4. Cancelling a repeating job 
5. Cancelling a one-off job

<p align="right">(<a href="#top">back to top</a>)</p>

-->

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

Wander Siemers - wandersiemers@me.com

Abel -

Florentin - 

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

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