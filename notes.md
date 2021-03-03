# Luigs & Neumann : SM1 Control Unit with Mini25-YL manipulators

## Units and resolution

Some comments: through the use of the "reset counter" command, I have zeroed the
coordinate of each motor to some middle (by eye) position. Then I moved manually
each motor from one end to the other. In each of these two positions, I queried
the coordinates and counted the total range of the movement span.

For one motor I got 5'732 steps and for the other 6'012.38 steps. Now, let's
assume that the full range corresponds to 25mm (i.e. 25'000 um): diving this
number by the total number of steps  gives the following results:

	- 25'000 / 5'732.00 ~ 4.36 µm/step
	- 25'000 / 6'012.38 ~ 4.15 µm/step

Instead, assuming the full range to be 30'000 µm, one gets:

	- 30'000 / 5'732.00 ~ 5.2 µm/step
	- 30'000 / 6'012.38 ~ 4.9 µm/step

From these considerations, I then infer that one 'step' corresponds to 4-5 µm.
The minimal movement (i.e. single CW or CCW step), being 0.01 step, thus corresponds
to 0.04 - 0.05 µm = 40-50 nm. This should be minimal resolution.


## Official response from L&N

On March 2nd 2021, L&N (Vedran Alilović) directly answered my question stating that:

0.01 step corresponds to 0.01 µm, suggesting 10 nm is the resolution of the system,
and that 1 step = 1 µm (instead of 4-5). This is only true for the LN Mini25 motors.

This would mean that (e.g.) 6'012.38 step (full range) would correspond to ~6mm,
instead of 30mm. This seems strange and I asked for further clarifications.


## Direct measurements of the 'step'

The use of a (calibrated) microscope, with 40x or 60x optics to reveal the position of
the tip of a borosilicate tip, seems the most ideal and conclusive means of direct
validation of how much one "step" is in micrometers.

There is another possibility, trading lengths with volumes. The latter, in fact, might be
easier to measure, especially in the case of a liquid and of Gilson precision pipettes.

The rationale is the following:

 - take a round Petri dish and measure accurately its diameter and thus radius (e.g. r = 5cm)
 - fill the Petri dish with some ringer electrolyte (e.g. equivalent volume V1) up to a level h1
 - V1 = pi r^2 h1, where h1 is thus the height of the "cylinder" of the solution in the dish
 - Say that we have some method to measure the manipulator coordinate corresponding to h1
 - Adding some further liquid to the dish, will raise its level from h1 to h2 (by dh = h2 - h1)
 - For this, we need to add to go from volume V1 to V2, where V2 =  pi r^2 h2 = pi r^2 (h1 + dh)
 - It is easy to show we must add to V1 a quantity that is dV = (pi r^2 d).

	 Therefore, if h1 = 100 um = 10^-4 m = 10^-2 cm, then dV = 0.785 cm^3 = 0.785 ml.
	 If we can measure with some high degree of accuracy (i.e. Gilson pipette) 785 ul, then we
	 can raise the level of the Petri dish electrolyte of 100um.

Now, the method to get the micromanipulator coordinate corresponding to a certain height of the
electrolyte in a dish, is based on the fact that if the pipette attached to the micromanipulator
is filled by an electrolyte, as soon as the tip touches the level of the liquid, the electrical
circuit between the pipette and a reference electrode in the bath will be closed. Such an event
can be easily detected electrically (e.g. by an oscilloscope).


The test we made, with Matteo, led to the following results: 'delta' was measured in the
coordinates of the micromanipulators (i.e. steps):

delta = 35.83  corresponding to ~100um; therefore 1 step = 2.79 um

The test was repeated going "slowly" and leading to delta = 25.63, thus 1 step = 3.9 um

The latter, in particular, seems in good agreement with my earlier estimate of 4-5 um/step.




