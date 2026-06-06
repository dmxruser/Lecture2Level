# Lecture2Level
## Overview
Lecture2Level (Pronounced Lecture to Level) is a web application which it's entire and sole purpose is to make a completley boring lecture into a simplistic, yet fun level for the game "Geometry Dash"; using some clean python; sprinkles of libaries like ```librosa``` and ```numpy```, an elephant called ```moviepy``` which is just a big ```ffmpeg``` wrapper; and some nice ```Bootstrap``` , with a theme I found called ```cosmo``` from ```bootswatch.com```; causing some nice things. With a special meniton to ```Dropzone.js``` for the dropzone; even tough I just copy + pasted their example; and removed some parts. 

Special mention to the ```GDShare``` project by HJFod for providing nice .gmd's to quickly put and go in the game geometry dash; and ```Jukebox``` for providing a way to quickly drop in audio files without going trough five layers of hell; and the ```Geode SDK```, for the SDK behind all of this.

## How do you use it?
Pretty simple actually! When you open an instance of Lecture2Level; you drag and drop your file (or browse it if your browser just doesn't...), choose your speed from the dropdown; and click the "Convert to Level" button; for longer files, and ESPECIALLY VIDEO FILES; this might take a bit, so go drink some coffee while your at it, or pet your Flareon; it's your choice. Once it's done; you can download the .gmd and .mp3; and go read the links for more information on how to use it?

## Why did you choose what you chose? 
To explain my choices; I have to explain that a lot of the code is server-side instead of client-side; meaning that quite a large amount of this codebase must be fast enough to not take hours; not crash as soon as somebody dares to try to run more than one file at a time? So; what gives? ```librosa``` was a must have; since it made the process of using audio files and bringing calculations to ```numpy``` a breeze; while being lightweight at the same time. ```numpy``` is an expected dependency due to it's usefullness in calculating many mathmatical things at the touch of a few functions combined; while still lightweight; it is not as lightweight as I'd like it to be; but is still much better than the alternative. ``moviepy`` was a simple libary to add; as all it does in this project is simply convert mp4s to mp3s; which does take a while because it is O(n) in terms of time complexity; so you'd have to sit for a while. A major reason I decided to import moviepy is that it's a small wrapper just for ffmpeg; which is a great choice here.

## Can you explain the file choice?  
There are a total of 4 important files here; with some being much longer than others; going from smallest to largest in terms of lines of code.

### lhelp.py
```lhelp.py``` is a small file with around 28 lines of code; which has two functions. ```makedata(file, distance)``` is a simple data maker for adding distance to a specific chunk of level, by using semicolons (;) as a seperator between each object; checking for each entry in entries; and splitting each one based on commas (,); then we check if the lenght of the file is above three to prevent errors; after checking, we quickly convert it to an int to add the distance to it; then converting it back to a string and appending it back; and returning a list called entry with a semicolon at the end to make sure it doesn't crash the game.

### fhelp.py

```fhelp.py``` whould have been a short file at 19 lines long; if ignoring what's in the last function. ```encrypt_file(file, output_path)``` does what you whould expect; encrypts the file by compressing it with gzip; then encoding it in Base64; returning the outputh path of written and encrypted file.
```output_file(fileoutput, data)``` is even simpler; writing some data using fstings as a simle way of inputting the name and actual data. In the end; this returns at 42 lines because of said fstring. nice.

### shelp.py

```schlep.py``` is a somewhat complex; but since we're near the end of this readme; we can shorten things up a bit. ```convert(filename)``` is a simple function that converts an mp4 to an mp3 using moviepy's VideoFileClip; writing the audiofile using the audio track; converted by the codec ```libmp3lame```. ```speed_up(input_path, output_path, speed_factor)``` is another simple function; using librosa to load the file; speed it up using it's time strech function; writes it to a temporary file; and returns it. ``load_song(filename)`` does what you whould expect; loads a song under a filename. ```calc_average(arr, smpl)``` does the same thing; uses a mix of np.average and np.abs using arr to calculate the average. ```get_lenghts(arr, smpl, avg)``` uses a threshold as a range for the average; and chunks it using some cryptic averaging I had to ask stack overflow for... Some ifs calculate if its higher, is, or lower than the average; and puts 1, 2, or 3 corespondingly in the list; and outputs said list.

### app.py

``app.py`` is your usual app.py; routing functions; which are easilly readable if you know the above functios used in previous files; so yeah; cool right?

Yap Yap Yap THIS IS FINALY OVER OMG 869 WORDS