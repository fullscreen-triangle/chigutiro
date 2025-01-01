# Chigutiro
High performance pipeline for high volume audio signal processing, annotation, clustering.


## Neurofunk
Neurofunk, is a loose term for audio records that primarily satisfy to conditions, a fast 4x4 drum beat
enveloped inside an atmosphere of mostly hatred. Contrary to the accepted notion that the bassline is the root 
cause of the genre's signature sound, it is the drum kick that does most of the heavylifting towards the path to darkness.

In this paper 'The emotional characteristics of bass drums, snare drums, and disengaged snare drums with different
strokes and dynamics', data from a listening study was analyzed using linear regression. From the study, the bass 
drum was strongly correlated with almost all negative emotions and inversely with high energy positive emotions.
The type of drum strokes, timing, groove and valence have secondary effects ranging from agitation and a sense of disturbance.
The feeling of Slapstick, associated with high energy positive emotions (playful, joyful or exciting), are related to 
to the brighter sounds of the snare drum. 

Why Funk ? Exposed to specific audio frequencies, humans experience an urge to move their bodies in a manner synchronized 
to the external audio source, or just simply groove (relative swing). A lot of factors have been found to be necessary for the existence 
of groove : microtiming, rhythmic syncopation, event density, beat salience, and rhythmic variability, expertise, taste, familiarity 
and one's proneness to dancing. Hence the reason why the genre is called Neurofunk, that is, groovy music aimed solely at one's emotions. 

## VIP or Dubplate 

Due to the nature of the genre, it is expected that, any master record, is at best, the result of an artist practising the highest 
form of self restrain, and in some cases, they fail to do so, and release a VIP (variation in production). Neurofunk artists only 
ply their trade in the form of a live or prerecorded mix, that is, an extended mixture of all the songs they intend on broadcasting.
In order for one to transition from one song to another, without an abrupt stop, sections from at least, the sequential tracks have to both be 
playing at the same time, at some point. How can one ascertain that, a song playing in a mix is a VIP or a Dubplate (unreleased song).
Dubplates are songs played by artists that were pressed on vinyl and meant to be played once and destroyed. Artists dedicate their lives 
to refining Dubplates and this is the tool required to make that critical distinction.

## Amen Break
In 1969, the Winstons, a multiracial soul and funk band from Washington DC released a 7 inch vinyl record with "Colour Him Father" on the A-Side 
and "Amen Brother" on the B-Side. The song features a 7 second long segment called the "break", that is, the literal break for all the other instrument 
players, except the drummer. If one where to buy two copies of the record, through vinyl scratching, one can elongate the 7 second segment to any 
length they wish. This is exactly what happened, with this specific record leading to the particular break sample being the most sampled sample 
in the whole wide history of electronic music. Any urban or electronic record that is broadcast in media, is based on the Amen break.

[Amen Break ](https://en.wikipedia.org/wiki/File:The_Amen_Break,_in_context.ogg)


## Pipeline

### 1. Mix Segmentation
The mix is segmented into candidate tracks based on:
- **Onset Strength**: Sudden increases in amplitude or rhythmic energy, detected using:

$$
O(t) = \sum_{f} \left| S(f, t) - S(f, t-1) \right|
$$

Where \( S(f, t) \) is the Short-Time Fourier Transform (STFT) magnitude at frequency \( f \) and time \( t \).

- **Energy Changes**: RMS energy is calculated for frames, and transitions are identified by significant energy differences.

---

### 2. Feature Extraction
Each segment undergoes:
- **Tempo Analysis**: Detecting tempo using beat tracking.
- **Rhythmic Metrics**:
  - **Event Density**: Number of rhythmic events per unit time.
  - **Beat Salience**: Strength of detected beats.
  - **Microtiming Deviations**: Variance in inter-onset intervals.
- **Harmonic Features**: Detecting the musical key and harmonic structure.
- **Bassline Extraction**: Isolating bass frequencies using harmonic-percussive separation.

---

### 3. Amen Break Alignment
The **Amen Break** acts as a "template" for comparison with tracks in the mix. It helps detect transitions and overlapping sections by aligning its **drum patterns** (kick, snare, hi-hat) to the track.

#### 3.1. Drum Pattern Extraction
For both the Amen Break and mix segments, drum patterns are extracted:
- **Frequency Ranges**: Separate kick (20–150 Hz), snare (150–400 Hz), and hi-hat (4000–10,000 Hz).
- **Onset Times**: Use onset strength to locate attack points.

#### 3.2. Alignment Using Cross-Correlation
The extracted patterns are aligned using cross-correlation:

$$
R(\tau) = \sum_{t} x(t) \cdot y(t + \tau)
$$

Where:
- \( x(t) \): Drum pattern from the Amen Break.
- \( y(t) \): Drum pattern from the segment.
- \( \tau \): Time lag.

The maximum value of \( R(\tau) \) gives the optimal alignment offset:

$$
\text{Alignment Offset} = \arg\max_{\tau} R(\tau)
$$

#### 3.3. Multi-Layer Alignment
Each drum layer (kick, snare, hi-hat) is aligned independently. A composite alignment score is computed by averaging the offsets:

$$
\text{Composite Alignment} = \frac{1}{N} \sum_{i=1}^{N} \text{Offset}_i
$$

Where \( N \) is the number of layers.

---

### 4. Similarity Analysis
A **similarity graph** is built to compare segments:
- **Dynamic Time Warping (DTW)**:
  
$$
D(i, j) = \left| x_i - y_j \right| + \min \{ D(i-1, j), D(i, j-1), D(i-1, j-1) \}
$$

DTW calculates the minimum cumulative distance between two feature sequences.

- **Graph Representation**:
  - Nodes represent segments.
  - Edge weights represent DTW distances.

---

### 5. Clustering
Segments are clustered using DBSCAN (Density-Based Spatial Clustering of Applications with Noise):
- **Core Clusters**: Tracks with high similarity (low DTW distance).
- **Outliers**: Tracks that deviate significantly (potential VIPs or Dubplates).

---

### 6. Outputs
1. **Segmented Tracks**: Individual `.wav` files.
2. **Heatmap**: Visualization of metrics over time.
3. **Mix Signature**: Graph showing relationships between tracks.
4. **Combined Metrics**: A JSON and CSV file storing all extracted features.

---

## Mathematical Foundations of the Amen Break
The Amen Break is treated as a "drum template," and its alignment relies on:
1. **Frequency Domain Analysis**:
   - Kick, snare, and hi-hat patterns are separated by their frequency bands.
2. **Cross-Correlation**:
   - Patterns are matched by finding the lag \( \tau \) with maximum correlation.
3. **Dynamic Time Warping**:
   - Handles temporal deviations in rhythm, ensuring robust alignment.

This allows precise detection of transitions, overlaps, and variations in the mix.

---

## Citations

[Zeyu Huang,Wenyi Song,Xiaojuan Ma,Andrew Brian Horner :The emotional characteristics of bass drums, snare drums, and disengaged snare drums with different
strokes and dynamics ](https://watermark.silverchair.com/035005_1_2.0001834.pdf?token=AQECAHi208BE49Ooan9kkhW_Ercy7Dm3ZL_9Cf3qfKAc485ysgAACBQwgggQBgkqhkiG9w0BBwaggggBMIIH_QIBADCCB_YGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMfXFdrnsN_y7_RS1pAgEQgIIHxygDB5isngmAdRd0dnPvvUFEyC8itZ9Sp17ThmpeC8ZuTP2cFft_eojSooy7_ykmA1Rl4xhu_i0ObkkAqmmm2iuDbhnmUJpVBaM1PooJUmz7YuEWRg3_WB9qQSUp3ZvI-lDLZ6ASsYSj_yakvRVsSenGqI-B4iKHolGgwJKTCsLl5LzdGjQ_G5XdwFzlAYd7l4R7PU1Gu0UyEhx2O7PMN4K-LDReXWn3Qqps_YnU2F9pJlkCBDNU2lJ4zprYUea4VhuHatbg1og4yMHDT1kc9w-HpgOJCtxh-MDcYqSM1_xLkKHM5kEGyD97dDmdvMDz9qQm5hmnYNDaE8TGx2T7_mmvq3HMcFCRzk4aG0zxYAYereVcxuswaoxqc8vdkHCC8PD83Qcyn1U0T2bwch-6IKTxfb7PKZ3cCmW5i1THqyK9DsdJ7HWscVhajzblFmz4Hi_evIho6rbRe2RTUfhNQHtm_im7ptN3OCPSOczpF3zOr81Nq35wXAHfIxwbReECMClpzaMtj7tbWz-D-ATQEKkFeXgpDXsuHaFchGGN_7QhmB2jHx9JDVBsO4QF3cizoiuIAfffQJhThsPhItDFIj_ivGmbGdlDmmSJMH1VBLVxwhCAj4E09__Wrsz8-2Rp_IDs6aGStcHqXIebqTK7M5_05sQ8oKqzCYe5lRBjAzLmLKcnXedDm52xEgEMO070obW_YBzk0kvG4yTg8go5kCpBXhORBpCUmgfTscKrsIIL2nnBGWnavE0TBd05d5eDuHVYKNO43cmRFO9pWVmn4sJiPsAuaGL1R65TLyCBkMqDZ1ByF2IKtuXDf318xHEmfU6yAddJpDNUTTitbZO9xJ8UCeUoaQVfs_XL7BGfqRt4-jGRb4qpvKW0pTzto5nl-wZGAe4rzkij_HSZ2pkhPJV2Lg2BYRiK7KaMqo75ImBoyWKRzHZLTlKuBK2_f1U_MKB8hcJX060P2Z9ySYu5I72OlZ0dtTp2qNbqVF8QdUleEnH5D_mhDJn3xLo6uXSlj_FqNcULf98cqEKsWDjeVaAXoBiy5X53ZW01DWSr9ntI69nmeGzD-LmFFHxAGTEC7ZAQUznSeVoi_FkffUGwngHkqQ08wvBNBgx4-GM0yYs1qnF8CVsYKJfa8XHVpEicqomYrCuk-IYvsuCC7h7uiX0DJGbz_y9uJtGr-xN0KMVsWAXy0J0njJBOH4oEePGOGwTR3ixMkxwq8rnIqdlJLYVr3vYQras8z3uzjIHt5EAtxAHQmZER-oAhZj9zfEsmLDz6ifyabgQBfFo_NAPWKNu_XU9ZI_YNY7oJunX1ZfFzGwXPHCsZ3rrqOB86TysiBmbGCpIK2fj2AFBsPI37q8rIg8f4PQVuPcKdk94de4mZTcjx7qSvtldVtYz8JMduSViuhLC1HhY6Dy47MNf9fh9IWAs_xe1xK3grT1UpzZem6eSeDkL96kpiUIrOu74WRjYbYZ0kPj8Fi2joWX2PPJHZM_gkgSrY5dmdi54gyOIEbvJO3Al7TAAEgNXH5krhEVuMmcVPl0ONYD4Nyyw4SgX6W4N58_gr9fpNPO4_730tVn4Ka3E2472QuH9lHaDBk61mH3ZSQWftDeeH7ZTD0m1Vf63yineM64cL_0W0AXc0Ga8nnC0w_dyqy1Lo_3bUZDZbDDdGZLLrLdJMfCJrgLb7w8nwTbdnwZP_Lotx_1IKCLKyS4Nig6S4_ASNyOWGqZt_0s-JeN5CC2B2dUC8zNgY-YWDVY22-_VTZICKu6X1GFr5UzkVOVQHhOekGisLoTdyAwSPlCP4EZT3KmlbyUKLNku2nx7yd6-TbRrsNg8kcUhF8-8xXQihFYD2N9LTuNEdakPKErv1oekmKxggsIofBlQPxDFosboVpG9hcTA1vOFVkzyrZn0o5abNOU8z1c9JoA6J1QWYu6P-dSgZHVxVjjOv-RnBhmEuET8RTdhUxBiSxWnYNGNegWXvQjPC88jXe4dAzoQ0t5PpIpysfQ0rSdpOgrYbLvtvMPh8gYC9G1SExsF7kuuRnFKVxJ85Lf4SR-iBSkUUZ5whtwdmAAUji4a8QyeBM5YMy5NU1jQCn1-g2iKIO5XCDN3Zo-8OqUAuwGtKS_iA5-RiAoaN-3Xn5EoOiSAnedYDLnU0I12IzU_NV2T6z7ylwShbXA8D7z8bMQChpt4rvyCfC3AA7TxFjPc7RqPmmVOJrU4DFU0rRbokj6re9PV6UoiyuHpMqC6yczPEktZCgdIYfI43ZU_K7PE9farc-j8QPOqFkN48JLnRUo2ZY4zocGFoHDp7J1QhfawjUlSSjK8SIVdpZwcRd8zXnG9AXGJwiudXXPGSsy_gFQzMM1RQ6gbQ54TVGH955-2qWxIdCaUgcX_05aRBSzjFepGEWz8CdyuilflmLLQ53nRq7RafP3iGnqwJRZsdTUkNE4FkIviKENvu4nGE37kTThhq60ZiWhiwzt3U30oyxqbKVXP7i9GyQ-lxmsb2RkXK0DZfekatgTD7k1U4oXDtwWWSOBhNoCxgms7jEXvylMkXwDIVdcO4MfM2fuamt_B8BrPEQqFEaPjBQF2SVFnVWZ2D-AYGEH3ZgLcrH1OutRE60dBUvtvR-S17E5EXsEES63PjdGqdasOAoAyR2c4XATCc)

[Olivier Senn,Lorenz Kilchenmann,Toni Bechtold,Florian Hoesl : Groove in drum patterns as a function of both
rhythmic properties and listeners' attitudes](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0199604&type=printable)

## How to Use
1. Place your mix file (`.wav`) and the Amen Break (`amen_break.wav`) in the working directory.
2. Run the pipeline:
   ```python
   from pipeline import analyze_mix
   analyze_mix("path/to/mix.wav", "path/to/amen_break.wav")
