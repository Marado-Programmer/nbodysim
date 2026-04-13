#set quote(block: true)
#set cite(form: "prose")

= Introduction

#lorem(420)

#pagebreak()

= Physics

The branch of physics that we care about for this project are the Isaac
Newton’s classical mechanics and its laws of motion, I believe.

When I had to learn this at school, Wikipedia @wikipedia_main and CrashCourse's
YouTube's playlist on physics @crashcourse_physics_playlist made me understand
mechanics.

Let's try to summarize the basics.

== Kinematic Equations

Every object has its _position_, like it's coordinates, represented by $r$.

When that object is in motion, there is a _velocity_, $v$, that is, the _speed_
of the object in a certain _direction_. When there's no motion, $v = 0$. This
speed and velocity are normally represented as the magnitude and direction — in
Portuguese _sentido_, since _direção_ alone doesn't let us represent the
inverse of a vector — of a vector respectively.

Given a constant velocity (no acceleration) $v$, $r = r_0 + v Delta
t$#footnote[@yt_motion_video], $r_0$ being the initial position, $Delta t$
being the time passed, so $r$ is the position when the object moves with that
velocity $v$ for $t$ units of time.

Because $r$ varies over time, we can say that there is the function $r(t)$.

The average velocity is $macron(v) = frac(Delta r, Delta
  t)$.#footnote[@wikipedia_velocity] When we close that time window to a
certain point of time, we tend to get the velocity at that point of
time.#footnote[@yt_derivatives_video] The velocity at given time $t$
(instantaneous velocity) is represented as:

$ v(t) &= lim_(Delta t -> 0) frac(Delta r, Delta t) = \
    &= lim_(Delta t -> 0) frac(r(t + Delta t) - r(t), Delta t) = \
    &= frac(d r, d t) = r'(t) $

Velocity changes position over time, and acceleration changes velocity over
time.

So something similar happens to calculate the acceleration $a$:

$ a(t) &= lim_(Delta t -> 0) frac(Delta v, Delta t) = \
    &= frac(d v, d t) = v'(t) = \
    &= frac(d^2 r, d t^2) = r''(t) $

Because we don't like in a unidimensional world, $v$ and $a$ are represented
in vectors:

$ arrow(a) = frac(Delta arrow(v), t) &<=> arrow(a) t = Delta arrow(v) <=> \
    &<=> arrow(v) = arrow(v_0) + arrow(a) t $

We can also use integrals to arrive to some common
equations:#footnote[@yt_integrals_video]

$ arrow(Delta r) &= integral^t_t_0 arrow(v) d t = \
    &= arrow(v_0) t + frac(Delta arrow(v) t, 2) = \
    &= arrow(v_0) t + frac(arrow(a) t^2, 2) $

And from that, we arrive to the kinematic
equation#footnote[@crashcourse_motion] $r &= r_0 + arrow(v_0) t + frac(1, 2)
arrow(a) t^2$.

=== For Later

There are some equations that appear on the project statement that we can talk
about right now.

We can calculate the new position of an object if we have a record of the of
it's last its position, velocity and acceleration at a certain point of time.
We then know how much time has passed, so from the last equation we get:

$ r(t + Delta t) = r(t) + v(t) Delta t + frac(1, 2) a(t) Delta t^2 $

We can do the same for the velocity:

$ v(t + Delta t) = v(t) + a(t) Delta t $

On the project statement, the teacher suggests a _half-step_ and finally a
correction. I still have to figure out why exactly, but the logic is the same.

== Newton's Law of Universal Gravitation

This part about the history of the apple falling on Newton's head, we are
learning together! Or at least I'll relearn something that didn't get stuck in
my head this last year's I had physics in school.

#quote(attribution: [@wikipedia_gravitation])[
  Newton's law of universal gravitation describes gravity as a force by stating
  that every particle attracts every other particle in the universe with a
  force that is proportional to the product of their masses and inversely
  proportional to the square of the distance between their centers of mass.
]

That gives the following:

$ F_"gravity" prop frac(m_a m_b, norm(arrow(a) - arrow(b))^2) $

With empiricism, Newton figured out that the bigger the masses of the objects,
the stronger the force; and the further apart the objects are from each other,
the weaker the force.

Well, one thing is for sure: I am not some sort of magnet that when I'm walking
around things just come towards me, and I only walk into a streetlight by the
force of distraction, not by some sort of gravitational force. At the same time,
when I fall, I find the ground and not the sky. Right. Newton came to the
conclusion that the force between me and the Earth’s surface (between me and
the Earth really) is much, much greater than the force between me and...
Imagine something really, really, big, and probably heavy, like a whale, or a
huge building, the biggest in the world. That mass is nothing compared to the
Earth’s mass. But certainly there are heavier things than the Earth, right?
Probably the Sun, for example. Yeah, probably, but don't forget that we are
touching the Earth, and *the Sun is probably an astronomical unit away*, and
that the distance between the objects also count.

Because of all of the above, Newton added to the equation a constant $G$ which
represents just a very little and tiny number that would make those force
calculation results seem more realistic. $G$ initially didn't have a specific
value attributed to it by Newton. Later scientists figured out that a good
number for it is $G = 6.6743015 times 10^(−11) "m"^3 "kg"^(−1)
"s"^(−2)$.#footnote[@yt_gravity_video]#footnote[@wikipedia_gravitational_constant]
As Newton figured out, pretty tiny. So the formula becomes:

$ arrow(F_"gravity") = G frac(m_a m_b, norm(arrow(a) - arrow(b))^2) $

Look how cool is this. If you are free-falling, the force of gravity acting on
you, based on the second law of motion#footnote[@wikipedia_newton_laws], is:

$ arrow(F_"gravity") = m arrow(g) $

We are taught that the acceleration of Earths gravity is close to
$norm(arrow(g)) = 9.8 m"/"s^2$. Now look:#footnote[@yt_gravity_video]

$ frac(arrow(F_"gravity"), m_"you") &= G frac(m_"Earth", norm(arrow(a) - arrow(b))^2) = \
    &= arrow(g) = \
    &= vec(9.8) $

$norm(arrow(a) - arrow(b))$ is the radius of the
Earth#footnote[@wikipedia_earth_radius] (I guess the Earth isn't a sphere, but
you get the point), so:

$ G frac(m_"Earth", 6371008.7714^2) = 9.8 &<=> m_"Earth" = 9.8 frac(6371008.7714^2, G) <=> \
    &<=> m_"Earth" = 5.9598683 times 10^24 "kg" $

I believe I did the maths right, and as you can see, the Earth is... heavy.

= $n$-Body Problem

#quote(attribution: [@wikipedia_gravitation])[
  The problem of predicting the motion of n objects subject to gravity is known
  as the n-body problem.
]

#pagebreak()

= Conclusion

#lorem(67)

#pagebreak()

#bibliography("bibliography.yaml", style: "american-physics-society")
