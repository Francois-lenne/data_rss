import sys 
import os

import function.correct_r_code as correct_r_code

texte = """
<p>I'm trying to display a planisphere using a map from rnaturalearth library, and I want to add some X and Y axes on each side of my planispher, I managed to set up correctly the Y axes, but I can't find a way to correctly set up the X axis. Here is the result I got for now :</p>
<p><a href="https://i.sstatic.net/mAMvv8Ds.png" rel="nofollow noreferrer"><img alt="MapIGot" src="https://i.sstatic.net/mAMvv8Ds.png" /></a></p>
<p>As you can see the width of the X axes is equal to the width of the planisphere at 0° latitude, but I want it to have the same width as the planisphere at 80° latitude. I made the result that I want to obtain in the following image <em>(sorry about my poors paint skills)</em> :</p>
<p><a href="https://i.sstatic.net/DdVZnG14.png" rel="nofollow noreferrer"><img alt="MapIWant" src="https://i.sstatic.net/DdVZnG14.png" /></a></p>
<p>I'm sorry that you can't see the meridans lines, I don't know why the screenshot didn't show the meridian lines.</p>
<p>Now let's talk about my code, here is the library that I use :</p>
<pre><code>library(ggplot2) 
library(dplyr)
library(sf)
library(rnaturalearth)
library(rnaturalearthdata)
library(readxl)
</code></pre>
<p>And here is my code that generates everything :</p>
<pre><code>world &lt;- ne_countries(scale = &quot;medium&quot;, returnclass = &quot;sf&quot;)

longitudes &lt;- longitudes &lt;- c(-180, -140, -100, -60, -20, 0, 20, 60, 100, 140, 180)

# Créer les données pour les labels de longitude (axe X)
bottomXAxis &lt;- lapply(longitudes, function(x) {
  st_sf(label = paste0(abs(x), '\u00b0'),
        geometry = st_sfc(st_point(c(x, 0)), crs = 'WGS84'))
}) %&gt;% bind_rows()

topXAxis &lt;- lapply(longitudes, function(x) {
  st_sf(label = paste0(abs(x), '\u00b0'),
        geometry = st_sfc(st_point(c(x, 0)), crs = 'WGS84'))
}) %&gt;% bind_rows()

nudgeXValues &lt;- rep(0, length(longitudes))


# Créer les données pour les labels de latitude (axe Y)
leftYAxis &lt;- lapply(c(-80, -60, -40, -20, 0, 20, 40, 60, 80), function(y) {
  st_sf(label = paste0(abs(y), '\u00b0'),
        geometry = st_sfc(st_point(c(-180, y)), crs = 'WGS84'))
}) %&gt;% bind_rows()

rightYAxis &lt;- lapply(c(-80, -60, -40, -20, 0, 20, 40, 60, 80), function(y) {
  st_sf(label = paste0(abs(y), '\u00b0'),
        geometry = st_sfc(st_point(c(180, y)), crs = 'WGS84'))
}) %&gt;% bind_rows()

nudge_left_y &lt;- c(-1.6e6, -1.2e6, -0.8e6, -0.4e6, -0.2e6, -0.4e6, -0.8e6, -1.2e6, -1.6e6)
nudge_right_y &lt;- c(1.6e6, 1.4e6, 1e6, 0.6e6, 0.4e6, 0.6e6, 1e6, 1.4e6, 1.6e6)

# Affichage de la carte avec les labels de longitude et latitude
world %&gt;%
  ggplot() +
  geom_sf(color = &quot;black&quot;, linewidth = 0.1) +
  geom_sf_text(data = topXAxis, aes(label = label), size = 3.5, color = 'black',
               nudge_y = rep(9e6, length(topXAxis$label)),
               nudge_x = nudgeXValues) +
  geom_sf_text(data = bottomXAxis, aes(label = label), size = 3.5, color = 'black',
               nudge_y = rep(-9e6, length(bottomXAxis$label)),
               nudge_x = nudgeXValues) +
  geom_sf_text(data = leftYAxis, aes(label = label), size = 3.5, color = 'black',
               nudge_x = nudge_left_y) +
  geom_sf_text(data = rightYAxis, aes(label = label), size = 3.5, color = 'black',
               nudge_x = nudge_right_y) +
  coord_sf(crs = &quot;+proj=robin&quot;, expand = TRUE) +
  theme_minimal() +
  theme(axis.title = element_blank())
</code></pre>
<p>I tried several options as scale_x_continous with xlim, but it didn't work, I hope someone will have the solution. Also I'm still a beginner in R programming so don't hesitate if you have any other feedbacks about my code.</p>
<p>Thank you !</p>
"""

code = correct_r_code.add_comment_code(texte, "# ")

print(code)