# StoryToolkitAI Features Info

[Click here to the main project page](https://github.com/octimot/StoryToolkitAI)

###  This page might contain references that are outdated, but will be updated soon!

## Transcriptions

### Transcription Results
The results we get with Whisper are significantly better than other Speech-to-Text model (including Google, AWS
etc.) out there **and the models are free to use**. According to OpenAI, the models have been trained on data in 98
different languages (cca. 65% of data in English) **and show strong Automated Speech Recognition results in ~10 
languages**. More technical blabla on the 
<a href="">
[OpenAI Whisper Github](https://github.com/openai/whisper/blob/main/model-card.md) or the 
[Scientific Paper](https://cdn.openai.com/papers/whisper.pdf), for hardcore enthusiasts. 

The magic takes over even for the most difficult noisy low bitrate stuff you can feed it - like recordings of your
assistant editor complaining about you without realizing that their back pocket is sending voice messages to random
people from their contacts list.

The results are really good for at least 10 languages, but remember, this is a machine doing transcriptions for you. 
And machines, just like unpaid interns have dreams too... For example, on longer periods of silence in your audio, you
may expect to see words that aren't there. Also, for uncommon names, it might give you nicknames instead, just to
mess with your feelings.

### Transcription Speed
We used the expression "runs like butter" above. There's one thing you need to know about butter - it's good when it's
fresh, but when it gets old it might get clumpy and smelly. Similar, the more state-of-the-art your machine CPU or
GPU is, the faster you get results. Please don't use this on your grandpa's Pentium 4 from the closet.

**Totally unscientific anecdotal tests:**

**Macbook Pro M1 8-core 16GB RAM** - 30-second timeline transcribed in cca. 45 seconds (1.5x time length of audio)

**Windows Workstation with GTX1070** - 60-second timeline transcribed in cca. 20 seconds (0.25x time length of audio)

We also received reports of transcriptions on RTX GPUs needing around 0.05-0.10x the time of the audio. So if you're
editing faster than that, please stop, you're embarrassing the rest of us.

### Quick how-to transcribe:

The following process assumes that you have Davinci Resolve Studio installed (not the free version of Resolve). 
However, **the tool also works independently without Resolve on the machine**.

#### 1. Open Resolve and StoryToolkitAI
Open a project in Resolve and then StoryToolkitAI
(or the other way around... why not make it harder for yourself?)

#### 2. Open the Timeline and Press Transcribe 

Go to Resolve and open the Timeline that you want to transcribe, then click the "Transcribe Timeline" button.

#### 3. Wait a bit

Your current timeline will automatically render to Audio Only WAV, and then a window with the transcription settings
will pop up. 

Enter the transcription settings (more info about settings 
[here](https://github.com/octimot/StoryToolkitAI#transcription-settings)) and then hit "Start".

Once the process has started, it needs a bit of time to transcribe. After all, there is a human-like AI trapped in your
machine doing your job for you on a mechanical typewriter with missing keys... It has the right to have day-dreams too.

As soon as it's done, the transcription will be saved on your machine.

_Important Note: **The first time you transcribe something**, it will take a bit longer to start the process
because Whisper needs to download the model file (around 1.5GB for the medium model) to your local cache. But, after 
the model is saved on your machine, transcriptions will take less._

#### 4. Transcription Finished
When the transcription is ready, a Transcription Window will pop up, showing you the transcript and allowing you to do
all sorts of magic things, like:
- linking the transcript to the current Resolve timeline
  (which will automatically open the transcript whenever you open the timeline in resolve)
- importing the generated SRT file into the current Resolve bin. 
- searching words or concepts in the transcript
- clicking on phrases to take your Resolve playhead on the right timecode
- etc.

_Less Important Note: Please make sure you sit down and have a glass of fresh water next to you when you see your first
transcription using OpenAI Whisper. Don't worry, the water coming down your cheeks are tears of joy. In the likely case
of hyperventilation, take a deep long breath and drink a bit of water. But, yet again, if the transcription is not above
average, don't despair, it's better to be prepared than sorry._

---

### Transcription Settings
Before starting the transcription process, you can tweak different options, including selecting the source language of
the footage, choosing between different Whisper models, the processing device, etc. For faster and better results,
we recommend at least selecting the source language.

_Note: when selecting "transcribe+translate" as "task", the tool will add both a transcription and a translation job to
the queue, as if you selected them individually. The translation will not use the previous transcription process results
at all, so this means that the process will take 2x the processing time._

For details regarding the models and their performance, please check 
[this section from the OpenAI Whisper repo](https://github.com/openai/whisper#available-models-and-languages).
Also, keep in mind that if you're transcribing on a CUDA device, you need minimum 5GB of VRAM for the medium model, and
minimum 10GB for the large model.

**Initial Prompt**. This is useful if you want the
transcription algorithm to adopt a certain style (for eg. separating speaker sentences, or using caps after 
punctuation), or even prime it to use certain names (for eg. "Helena" instead of "Elena"), or avoid rookie mistakes 
(for eg. showing "Hey, Wood!" instead of "Heywood"). The default prompt separates speaker sentences and uses caps after 
punctuation. 
Remember: this is kind of like telling your assistant editor "do that", but it's up to them if they want to follow your 
instructions or not - welcome to the wonderful world of AI. This feature is super experimental - it might even accept
instructions like "separate speakers" or "make me coffee", but you have to try it on your own.

**Pre-Detect Speech** - when enabled, the tool will try to detect speech-only parts in the audio and send only those
parts to AI for transcription. This reduces the transcription time, but should also help avoid hallucinations on 
silent parts of the audio. However, the AI might lose context from one speech segment to the next, so the quality
of the transcription might take a hit.

**Increased Time Precision** adds more precision to the transcription timestamps, but it increases the processing time.
For best results, we recommend using the large model with this option enabled.

**Max. Characters per Line** and **Max. Words per Line** make the tool split the transcript segments at the specified
number of characters or words. This is useful if you want to make sure that the transcript segments are not too long,
but since there's no AI involved in this process (yet), the tool might split sentences in the weirdest places.
When both options are set, the Max. Words per Line is ignored. 
Only works if Increased Time Precision is enabled.

**Split on Punctuation** splits the transcript lines at the punctuation marks set in the Preferences 
window - the default punctuation marks are: `. ! ? …`
This might not always be the best option, for eg. if your text contains many abbreviations (Dr., Mr. etc.),
but you could still activate it and then manually fix the transcript afterwards. We're looking for ways to improve this 
using AI. 
Only works if Increased Time Precision is enabled.

**Prevent Gaps Shorter Than** allows you to specify a minimum duration for the gaps between transcript 
segments. If the gap between two segments is shorter than the specified duration, the end time of the previous segment 
will be extended to the start time of the next segment. This is useful especially if you want to avoid having too many 
small gaps when using the transcript for subtitles.

**Time Intervals** allows you to selectively transcribe only a portion of the timeline and Exclude Time Intervals allows 
you to exclude certain portions of the timelines. The recommended format for these two fields is: "0.00 - 0.00".
For eg., if you want to transcribe the first 10 seconds of the audio and the portion between 30 and 40 seconds, 
you would enter this in the Time Intervals field:
```
0.00 - 10.00
30.00 - 40.00
```

#### Resolve "transcription_WAV" Preset

If you're transcribing timelines directly from Resolve and prefer to save them in WAV instead of MOV,
go to the Resolve Render Page, select the Audio Only preset, make sure that the "Export Video" in the Video tab is
disabled, then, in the "Audio" tab, select the "Wave" format and "Linear PCM" as codec. Then save this preset as
"transcription_WAV", and the next time you transcribe, you should see Resolve rendering wav files.

As a matter of fact, you can use any preset you want, as long as it renders audio too (Linear PCM preferred). For eg., 
if you want to render out an H264 proxy and include Data Burn-In with timecode info, 
just create that preset in Resolve and then modify the value of the 'transcription_render_preset' setting in the 
StoryToolkitAI config.json file in your user data folder (in the future, this will be editable from the GUI). Just keep 
in mind that before going through the transcription process, the tool will re-interpret the audio internally as Linear 
PCM (and you might need ffmpeg on your machine for that), so if you're using a CPU-intense codec, the process might 
take longer.

Another important thing to note is that your **audio channels are best left as Mono on your timeline and/or renders**, 
since the algorithm may ignore one channel or the other, and therefore only give you a partial transcription.

### Group Questions
You can click and wait for AI to detect and create a group with all the transcription
segments that look like questions. This is useful if you want to see all the questions in your transcript, for
instance if you're transcribing interviews. 

Detecting questions seems like a trivial task, but our speech is sometimes so complex, that, while a human can easily
detect if somebody is asking something, a machine might not be able to do that. Think about all the languages that
don't actually use a question mark, but more importantly, think about all the times we're asking for information,
but not using a question at all...

Of course, because we're using AI, this might give out false positives or negatives, but in our tests we find it to be 
pretty accurate... even with sentences that are asking for stuff, but don't sound like questions.

_Note: When not using this with a CUDA enabled GPU, it might take a while for the classification process to finish.
Nevertheless, just have a bit of patience and eventually the process will finish. BTW, if you're using the git version
of the tool, you can check the progress of the classification process in the terminal._

### Re-transcribing Transcripts

In some instances you might want to re-transcribe a transcript, for example if you want to change the Whisper model,
or if the speech was in a different language for that particular portion of the transcript.

To re-transcribe the entire transcript, you need to have the transcription window open, and then press the key T on 
your keyboard.

To re-transcribe only a portion of the transcript, select which segments you want to re-transcribe, and then press the
key T on your keyboard - the tool will automatically fill the Time Intervals field in the Transcription Settings window.

You can also not select any segments, but press the key T and then manually enter the time intervals that you want
re-transcribed in the Time Intervals field.

_Note: our tests show that re-transcribing only a short portion of the transcript sometimes doesn't give out the best
results and most likely messes up with the transcript timings for that particular portion that you've re-transcribed. 
This is probably due to the fact that the Whisper model works better when it has more context to work with.
In these cases, try to use either a larger model, or provide Whisper with more info using the Initial Prompt. Let us
know what tricks you use to get the best results!_

### Transcript Word Find
Once a transcript is loaded, a basic find function (CMD/CTRL+F) will let you find words in the transcript and show you 
their position. Press "ENTER" to cycle between results. Once you find what you're looking for, simply clicking the 
phrase will move the Resolve playhead to the respective timecode (if connected to Resolve API).

### Transcript Groups

Starting with v0.17.5, you can group transcript segments together so that you can easily select them later if you need
to. To add segments to groups, select them with V (or CMD/CTRL+Click, or other selection shortcuts) and then press 
CMD/CTRL+G. To see the group list for each transcript, click CMD/CTRL+G while in the transcription window. From there,
you can also add group notes for each group. For eg. if you group certain segments on a certain topic, you can add
your notes on that particular topic in the group notes field. You can also use the groups to select all the segments
of a certain character and so on.

Until v0.19.0, the Update Segments switch seen in the Groups window allows the user to automatically add segments to
groups when they select the segments in the Transcription Window. _Note: This will not remove any segments from the 
group, when they're unselected in the Transcription Window! In order to remove segments from the group, you need to 
update the group (for eg. using CMD/CTRL+G while the group is selected)_

Starting with v0.19.0, the Update segments switch in the Groups window allows the user to automatically update the
group segments when they select/deselect the segments in the Transcription Window. This will both add or remove
segments from the group.

_Note: the groups are based on time intervals, so if you change the start or end times of segments, they might drift
outside of certain groups that they're in. Simply click on the group, select the segments and press CMD/CTR+G again to
re-add them to the group_

While performing an advanced search on a transcription, the tool will also look in the group names and notes, and
will return the groups that match semantically to your search.

### Direct Translations to English
The tool also supports direct translation to English by clicking the "Translate Timeline to English" button. However,
it will not generate any original language transcription together with the translation, meaning that you'll have to
transcribe and translate in two different processes.

### Opening SRT Files as Transcripts
If you click on "Open Transcript" and select an SRT file, the tool will automatically convert it to a transcription
file and open it in the transcription window. This is useful if you want to use transcripts made by other apps in the
tool, for eg. to search through them, navigate and mark timelines in Resolve etc.

### Exporting transcripts as Fusion Text
Starting from version 0.18.3, you can export the transcription lines into a Fusion Text node.

1. Open transcription file
2. File -> Export as Fusion text...
3. Save .comp file on your drive
4. Open .comp file with notepad/text edit
5. Select all and copy all contents to clipboard
6. Open Resolve and/or Fusion (or Fusion page)
7. CMD/CTRL+V to paste Fusion nodes into composition
8. Then connect the new nodes wherever you want in your composition and modify the text styling

_Note: if using the built-in Fusion page in Resolve, we recommend using an Adjustment Layer instead of a Fusion 
Composition: drag and drop an Adjustment Layer into a new video track, over your entire timeline, right click and Open 
in Fusion. This way you can see the footage/effects/etc. underneath, plus you can hear the audio in case you want to 
adjust the text to sound further._

_Note 2: You can also open the resulting .comp file in Fusion instead of using the copy-paste method, but you will have 
to manually add whatever Input or Output nodes you need to make it work._

## Indexing Videos

Starting with version 0.19.2, the tool can also automatically detect and index scenes in videos using AI.
The index is used for searching of specific content in the video - more info on this feature coming soon!

## Advanced Search

Starting with version 0.19.2, the Advanced Search can also look into Video content - more info on this feature
coming soon!

Transcription windows have an "Advanced Search" button that will open up a separate search window. The system is now
quite experimental and very raw, but it will allow you to search transcripts almost like you search something on Google.
This means that whenever you enter your search term, the tool will try to understand its meaning and find the phrases
that have the most similar meaning. The results will be ranked by a score that takes into account the semantic
similarity with your search term. Once the results appear in the window, you can click them and the tool will select
the respective segment in the transcript and move the playhead to the respective timecode in Resolve (if connected).
CMD/CTRL+Click will select the segments in the transcript and allow you to mark them later in Resolve
(see Adding Markers section above).

There's also an Advanced Search button in the main window that will allow you to search in all the transcription and
text files you select. If you press Shift while clicking the button it will prompt you with a folder selection instead,
so you can actually feed it multiple transcription from different directories.

This is basically like having a search engine on your machine.

You can also pass multiple search terms, using the | (pipe) character to separate them. For example, if you want to
search for "about life events" or "about sports", you can enter `about life events | about sports` in the search field. 
The tool will then search for each term separately and return separate results for each term in the same search window.

If you want to tell the tool how many results you want to see, just use `[max_results]` at the beginning of the search,
for eg.: `[20] about life events | about sports`. This will return the top 20 results for each term.

For now, the search relies on punctuation in the transcripts/files to separate phrases and feed them to the algorithm, 
but this will be improved in a future update by allowing AI to look deeper into the text.

**The quality of your results will depend on the terms you use for search**. Just like on a web search engine, you should
be kind of specific, but not too specific about what you're searching. For eg., if you want to search for phrases where
your characters are talking about "genders", you should probably use "about genders". Simply typing "genders" in the
search box, will probably also include people names since the alghorithm will think that names are related to genders.

Keep in mind that we're using a very basic algorithm for now, so the results might not be perfect, but it can **already
give you some really good results** if you prompt it right - remember it's a neural network behind the thing!
Feel free to be as descriptive as you want in your search, and try to tweak the search terms until you get the results
you're looking for.

More info about the commands you can use in the Advanced Search window can be found with the `[help]` command.

_Important Note: **The first time you use this feature**, it will take a bit longer to start the process because the 
tool needs to download the model file (around 500MB) to your local cache. But, after the model is saved on your
machine, the search should work almost in real time._

_About search speed: the search is pretty fast, but it will depend on the size of the files you're searching. 
Using a lot of them will make the search slower, so a smaller transform model is recommended (more on that later). 
The first time you open a window and search something, it will take a while to turn the data  into something that the 
machine understands, but after the first search is completed, all other searches should work fast._

## Assistant

This feature is currently only available for Patreon Frequent Users and Producers -
more info on [patreon.com/StoryToolkitAI](https://www.patreon.com/StoryToolkitAI)

The Assistant is basically an interface to OpenAI ChatGPT (or gpt-3.5-turbo).

### Obtaining an OpenAI API Key

First, you need to have an OpenAI API key to use this feature. 
You can get one by signing up on [OpenAI.com](https://platform.openai.com/signup/), 
and then creating a new secret key on the [API Keys page](https://platform.openai.com/account/api-keys).
Make sure you keep this key safe, as it will allow anyone to use your OpenAI account on your expense!

Once you have the key, just add it in Preferences -> OpenAI API Key. 
This will be saved locally on your machine, so only people who have access to your machine will be able to see it.

### Usage and billing

Depending on the account you have with OpenAI, you might be charged for using the API, most likely using the token 
system they have in place. For more info on how OpenAI billing works, 
please check their [pricing page](https://openai.com/pricing/).
StoryToolkitAI is not responsible for any charges you might incur by using the Assistant, 
and we are not affiliated with OpenAI in any way.

To find out how many tokens you've used within the Assistant window, just type `[usage]` in the Assistant window
and you'll get a cost estimate. Again, this is just an estimate, so you should check your 
[OpenAI Usage page](https://platform.openai.com/account/usage) to see the actual cost.

### Assistant window

You can access the Assistant either by clicking on "Assistant" in the main tool window, or from a Transcription Window. 
(available only in version 0.17.18)

If you want to use a certain portion of the transcript as the context for the Assistant:
1. Open the transcription
2. Select the lines that you want to send to the Assistant using the 'v' key
3. Press Key O (not zero) to send the selected lines to the Assistant. You can also use SHIFT+O to also include the 
times or timecodes (if Resolve is connected) together with the lines to the Assistant.
4. The Assistant window will open and you can start typing your questions.

More info on the Assistant can be found by typing `[help]` in the Assistant window.

### Quick tips for using the Assistant

The possibilities here are endless. Feel free to use natural language to ask anything.
You can use the Assistant to:
- Ask questions about the transcript (characters, locations, events, etc)
- Summarize (try typing `tldr;`)
- Deduct certain things from the transcript (try typing `what is the main conflict?`)
- Understand the emotional tone of the transcript (try typing `how is the tone?`, `what makes this scene sad?`, `are the characters polite to each other?` etc.)
- Get ideas about what to ask the characters (try typing `what should I ask the character?`)
- Get ideas about possible outlines (try typing `outline the plot described in the transcript, each line should be a scene`)
- Get ideas about possible storylines (try typing `what is the main storyline?`)
- Even get you a .srt subtitle file (after sending transcript lines with times (SHIFT+O) try typing `subtitle this in .srt format`)
- Ask about the deepest black hole in the universe (try typing `what is the meaning of life?`)
- Anything else you can think of!..

Also remember to use `[reset]` as often as you can, so that you don't send the whole conversation to the Assistant 
over and over again, unless you're trying to follow something relevant from the previous messages.

## Story Editor

The Story Editor is essentially a screenplay editor that also allows you to select or collect segments from different 
transcripts and then export them as EDL or XML so that you can import them into your NLE and start editing.

To select transcript segments:
- add transcript segments by selecting them in the Transcription Window -> right clicking -> clicking "Add to Story"
- or, you can add them by right clicking any of the search results in the Advanced Search window and clicking "Add to Story"

We're currently working to implement adding the indexed video segments (and results) to the Story Editor too.

### Using Fountain syntax in the Story Editor
We recommend using the Fountain syntax for writing your screenplay in the Story Editor. 
This way, you'll be able to export as a .fountain file and convert it easily into PDF, or even import it into whatever
screenplay software you're using.
More details on [fountain.io](https://fountain.io/syntax).


### Exporting to EDL or XML

The story editor can export to EDL or Final Cut Pro XML files if you click File -> Export story as EDL or FCP7XML...

#### Export Settings
**Name** - the name of the EDL/XML timeline/sequence.

**Start Timecode** - the timecode that will be used as the starting point for the EDL/XML.

**Frame Rate** - the frame rate that will be used for the EDL/XML.

**Use Timelines** - if checked, the tool will use the timeline name of the media instead of the source media name 
in the CLIP NAME field of the EDL. For eg. for Resolve EDL imports, this will make Resolve use Timelines (Compound Clips)
instead of the source media, if the Timelines have the same name as the timeline used in the original transcription in 
StoryToolkitAI. _This is not yet implemented for XML exports._

**Export Notes** - if checked, the tool will export the fountain-style notes from the story (for eg. `[[some note]]` ) 
in the EDL.  For now, these notes are recognized by Davinci Resolve when you import Timeline Markers form EDL into the 
Timeline that you chose from the bin. _This is not yet implemented for XML exports._

**Join Gaps Shorten Than** - you can have the tool join gaps between segments that are shorter than a certain duration 
in frames. By default, the tool will join all clips that end and start on the same frame.

_Note: The Start Timecode and Frame Rate values are not stored in the EDL file itself. You'll most likely need to 
re-enter them when doing the import in your NLE (at least the Frame Rate)._

#### To import the EDL or XML into Resolve:
1. Go into the Media Bin you want the new EDL timeline to be, right click and select
Timelines -> Import -> AAF / EDL / XML / DRT / OTIO...
2. Select the EDL or XML file you just exported from the tool
3. In the next window, simply click OK (or select the options you want)
4. Select the bins where you want Resolve to look for the media and click OK
5. Now you should have an EDL or XML Timeline in your Media Bin

Important: every now and then Resolve refuses to find the media in the bins or the clips look all red in the timeline.
If that is the case, try to import the EDL / XML file one more time and it should work.

If you see that the clips in the sequence / timeline are offset, make sure that the start timecode for the media
clip in Resolve is the same as the start timecode of the transcription in StoryToolkitAI.

When importing an EDL file into Davinci Resolve, make sure you have the "Assist using reel names from the: Source clip filename"
option selected in Project Settings -> General Options -> Conform Options. This will make Resolve use the clip names
stored in the EDL file more efficiently. Also, we recommend only checking the bins most likely to contain the clips
you need for each EDL file.

_Known Issue: Combining media with different frame rates than the import timeline seems to be problematic when 
importing EDLs and XMLs into Resolve and might require additional manual work to make clips match the EDL/XML timecodes._

_Known Issue 2: Audio-only clips do not work at all with EDL imports in Resolve. In other words, audio clips will
not be imported into the timeline. So for those cases, we recommend using XML instead._

#### To import Markers via EDL into Resolve:
1. Go to the Media Bin where your timeline is
2. Right-click on timeline
3. Select Timelines -> Import -> Timeline Markers from EDL...
4. Choose the EDL file you exported from the tool
5. The lines from your story editor encapsulated in double-brackets (eg. `[[your note]])
should now be imported into the timeline at the right timecode(depending what segment it follows or precedes in the story)


## Davinci Resolve Studio integrations

_Note: The Resolve API integration is not available on the Free version of Resolve, you need to have a working Studio 
license installed on your machine to use this feature._

### Initial Setup

#### 1. You need Resolve Studio 18 or later
The free version of Resolve doesn't provide API access.

#### 2. Enable Local Scripting in Resolve
Make sure that, in Davinci Resolve Preferences -> General, "External Scripting using" is set to Local. 

#### 3. You need to have Python installed (also for the standalone version)

The tool connects to the Resolve API using Python, so you need to have that installed on your machine.

Make sure that whatever Python version you're using in your virtual environment to start the tool is not older than your 
most recent Python version installed on your machine - for eg. if you used Python 3.10 in your virtual environment, you
must make sure that 3.11 is not installed on your machine, otherwise the tool might not start or the Resolve connection
might not work!

**Using the standalone version** requires you to have either Python 3.9 (tool versions older than 0.19) 
or Python 3.10 (tool versions newer than 0.19) installed. If you have a more recent version of Python 
installed than what is required, the tool might not start or the Resolve connection might not work!

_Fixing Python installations:_ If you have Resolve installed on your system and it looks like you have the correct
version of Python too, but the tool or the connection to Resolve still don't work, you should first try to fix your
Python installation by simply re-installing it using the installer from [the official Python website]
(https://www.python.org/downloads/)

### Connecting to the Resolve API
Starting with version 0.18.1, the tool starts with the Resolve API connection disabled since many folks don't have
are not using the tool in connection to Resolve.
To enable the connection, use the top menu bar: `Integrations -> Connect to Resolve API`
You can disable the connection at any point from the same menu.

### Linking Transcriptions to Timelines
In the transcription window, the "Link" button will attach the transcription to the currently opened timeline in
Resolve. This will make the tool automatically open the right transcription when you switch between timelines in
Resolve. In a future update, this will also help the Global Search function know in which timeline, at what timecode
you can find the term you're looking for.

### Timeline Navigation via Transcript
Clicking on the transcript segments (phrases) will move the playhead to the respective timecode in Resolve.
UP/DOWN keys will also let you navigate between transcript phrases (see more transcription window shortcuts below)

### Adding Markers to Timeline via Transcript
You can now add markers that include the selected phrases in the transcript by pressing either M or SHIFT+M
(see more shortcuts below)

### Resolve Playhead to Transcript Sync
The tool highlights the transcript words at the current timecode in Resolve. To activate this function, simply press
"sync" in the transcription window and the words will be highlighted each time the playhead stops moving in Resolve.

_Note: we found some issues when synching timelines that have a frame rate of 23.976fps because of a bug in the Resolve
API. Unfortunately, the synching of these timelines might drift until Blackmagic solves the bug._

### Copy Timeline Markers to Same Clip
This copies the current markers to its corresponding clip in the media bin. 
Due to Resolve API limitations, it's important that the corresponding clip
is in the bin that is currently opened in the Media Panel. 
The clip's existing markers will be deleted before the new ones are copied!

### Copy Clip Markers to Same Timeline
Same as the function above, but in this case, the markers of the clip are copied to the timeline.

### Render Markers to Stills
This will render to TIFF and JPEG the first frame of the markers of a certain color or ones that start with a certain 
string. Works only on markers from the opened timeline. The first time you use this function, it should also add a 
Still_TIFF render preset in Resolve. This is necessary to render the stills in TIFF format, which then should get 
converted to JPEG if you have FFMPEG on your machine.

### Render Markers to Clips
This will render to H.264 the entire duration of the markers of a certain color or that start with a certain string 
from your currently opened Resolve timeline.

## Transcription Window Shortcuts

    Mouse Click     - move active segment on clicked text and move playhead to start of active segment

    CMD/CTRL+Click  - add clicked text to selection

    OPT/ALT+Click   - edit transcript segment
    
    Up, Down keys   - move the cursor up and down on the transcript (we call it "active segment")

    Semicolon (;)   - move playhead to start of active segment (or of selection)

    Apostrophe (')  - move playhead to end of active segment (or of selection)

    Colon (:)       - align start of active segment with Resolve playhead

    DoubleQuote (") - align end of active segment with Resolve playhead

    V               - add active segment to selection

    CMD/CTRL+A      - select all transcript segments (or deselects segments, if a selection exists)

    Shift+A         - create selection between the previously active and the currently active segment
                      also works to create a selection for the last played segments in Resolve (if sync is active):
                      for eg.: 
                      press 'sync', click a phrase, press play in Resolve, stop, then press Shift+A in the tool
                      
                      but,if text is selected in the transcript, the selection will be created between the first and last
                      segments of the selection.

    Shift+C         - copy transcript of active segment/selection with timecodes at the beginning of each block of text
                      (if Resolve is available)

    CMD/CTRL+Shift+C- copy transcript of selection with timecodes at the beginning of each transcript line
                      (or transcript seconds, if Resolve is not available)

    Backspace       - delete active segment (will ask for confirmation)

    m               - add duration markers for the active segment/selection
                      in case there are gaps between the text segments, 
                      the tool will create a marker for each block of uninterrupted text

    Shift+M         - add duration markers as above, but with user prompt for the marker name

    CMD/CTRL+M      - select all segments under markers filtered by color or name from the current Resolve timeline

    CMD/CTRL+Shift+W- close window

    Shift+L         - link transcription to the current timeline (if available)
    
    s               - enable sync
    
    Tab             - cycle between search and transcript navigation

    CMD/CTRL+E      - edit transcript

    Escape          - when editing transcripts, this will defocus and save the transcript
    
    t               - re-transcribe current transcription or selected segments

    CMD/CTRL+G      - add selected segments into new group

    CMD/CTRL+F      - open find window

    o               - send selection to the Assistant

    Shift+O         - send selection with timecodes to the Assistant

    CMD/CTRL+Shift+S- export transcription as...


Other shortcuts etc.

    Shift+Click on                      - allows you to batch transcribe multiple files                 
    "Transcribe/Translate Timeline"       from your drive instead of the current timeline
   
    Shift+Click on                      - allows you to select which folders to use 
    "Advanced  Search"                    for the advanced search corpus

    CMD/CTRL+Click on                   - selects all the lines containing the clicked
    search results                        result in the transcript window
                                              
                                                
## Execution Arguments

`--noresolve` - This will disable the Resolve API communication. 

`--skip-python-check` -This will skip the check for conflicting Python versions

`--debug` - This will show all the debug info in the console

---


# Known Issues

### First time using a feature takes longer
The first time you use a specific model, it will take a bit longer to start the process because 
the tool needs to download the model on your local machine. But, after the model is saved on your machine, 
the operation should take less. This applies to transcribing, indexing and searching.

### Hallucinations during audio silence
In some cases, on chunks of audio that are silent, Whisper sometimes writes phrases that aren't there. This is a known
issue. To prevent that from happening, try using the pre-detect speech option in the Transcription Settings Window.

### Tool doesn't start or doesn't connect to Resolve
If you have Resolve installed, there's most likely a conflict.
Please read the Davinci Resolve Studio integrations section above for more info.

### Tool freezing during Resolve playback
Currently, the tool gets stuck as it waits a reply from the Resolve API, while Resolve is playing back, but it gets
un-stuck as soon as the playhead stops moving. This will be fixed in a future update soon.

### Timecode issues with 23.976 timelines
A bug in the Resolve API which sometimes reports 23.976 fps as 23fps creates a bunch of issues mainly for operations
that use timecode (transcript to playhead navigation, adding markers at the precise frame etc.). Unfortunately, this
can only be fixed by Blackmagic within Resolve itself (fingers crossed for an update?)

### RuntimeError: CUDA out of memory
If you get this message while transcribing on the GPU, it means that your GPU doesn't have enough memory to run the
model you have selected. The solution is to either use a smaller model, or to transcribe on the CPU.

### Tool freezes when chatting with Assistant
The Assistant feature requires an active connection with OpenAI servers, which sometimes can be slow or unresponsive.
We'll try to improve this behavior in the future.

### Permission denied errors
If you get something similar to this error (or anything related to the .cache folder): 

  ```
  PermissionError: [Errno 13] Permission denied: '/Users/[your user]/.cache/torch/hub/trusted_list', 
  ```

it's most likely because due to some some ssl certificate issue (issue #77) , so it's best if you delete the old hub 
cache, like this:

#### On macOS
Open terminal, and execute

rm -rf /Users/USERNAME/.cache/hub
rm -rf /Users/USERNAME/.cache/torch
rm -rf /Users/USERNAME/.cache/whisper
replace USERNAME with your MacOS user

#### On Windows
Open CMD, and execute

rmdir /s /q C:\Users\USERNAME\.cache\hub
rmdir /s /q C:\Users\USERNAME\.cache\torch
rmdir /s /q C:\Users\USERNAME\.cache\whisper
replace USERNAME with your Windows user

Keep in mind that if you do this, the first time you transcribe or search something it will need to re-download the models, so it will take a bit longer.


### Please report any other issues
As mentioned, the tool is in a super raw state of development. Please report anything weird that you notice, and we'll 
look into it.