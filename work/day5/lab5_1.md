# Day 5, Lab 5.1: Decision matrix
 
| Approach | How it detects changes | Pros | Cons |
|---|---|---|---|
| Full load |  There is no detection and it reloads everything every time | Its simple as no tracking is needed | Slow and wasteful once the data gets bigger |
| Watermark | Track the highest last_modified seen so far and pull anything after it | Also simple as it only pulls whats changed | Misses deletes and breaks if last_modified isn't updated |
| CDC | Reads the database's own log, catches every insert, update, and delete | Catches everything including deletes | But more setup is needed for the database to support it |
| Source-event | Source pushes a message the moment something changes | Real-time so nothing is wasted | Needs the source to support sending events so that means more things to build |