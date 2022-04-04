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



## Usage

Some useful commands:

1. Scheduling a one-off job

   `$ cas myjob.py --repeat @daily`

2. Scheduling a repeating job

   `$ cas myjob.py --at 202204052230`

3. Listing all the scheduled jobs, repeating and one-off jobs

   `$ cas --list`

4. Cancelling a repeating job given the index

   `$ cas --cancel-repeating 42`

5. Cancelling a one-off job given the index

   `$ cas --cancel-one 42`

<p align="right">(<a href="#top">back to top</a>)</p>



## Roadmap

- [x] Schedule jobs
    - [x] Given estimate of duration and deadline
    - [x] Taking into account carbon intensity of the grid

- [x] List jobs
    - [x] Combined view of all jobs: one-off and repeating
- [x] Remove jobs given id of task
- [x] Implement offline model based on energymap's historical data on energy mix
    - [x] Location set to NL only
    - [x] Use time of the day
    - [x] Use day of the week
    - [ ] Use week/month/season of the year
- [x] Output saved CO2
    - [x] For current session
    - [x] For all sessions
- [x] Run parallel jobs
- [x] "Full of batteries basement" flag -> don't use energy data for scheduling
- [ ] Implement online/live model
    - [ ] Based on forecasting marginal carbon intensity
- [ ] GUI for non-technical users
- [ ] Windows platform support
- [ ] Extensive testing
- [ ] Consider machine workload

See the [open issues](https://github.com/abel-vs/carbon-scheduler/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

Wander Siemers - wandersiemers@me.com

Abel Van Steenweghen - Abel.van.steenweghen@gmail.com

Florentin-Ionut Arsene - arsene.florentin.ionut@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

* Luís Cruz - Assistant Professor at Delft University of Technology

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>
