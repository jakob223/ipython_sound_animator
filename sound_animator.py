from matplotlib import animation
from IPython.html import widgets
from IPython.display import display
from ipywidgets import HTML
import random
from tempfile import NamedTemporaryFile
import math
VIDEO_TAG = """<video controls id="video_{1}">
 <source src="data:video/x-m4v;base64,{0}" type="video/mp4">
 Your browser does not support the video tag.
</video>"""
AUDIO_TAG = """
            <audio controls="controls" id="{ident}" {autoplay}>
                <source src="{src}" type="{type}" />
                Your browser does not support the audio element.
            </audio>
          """
CONTROLS_TAG = """
    <input type="button" value="PlaySoundAndVideo" onClick='PlaySoundAndVideo("video_%s"),PlaySoundAndVideo("audio_%s")'>
    <script>
    function PlaySoundAndVideo(soundObj,videoObj) {
    var soundAndVideo=document.getElementById(soundObj,videoObj);
    soundAndVideo.play();
    }
    </script>
"""
def new_html(audio,uniq_id):
    return AUDIO_TAG.format(ident="audio_"+uniq_id,src=audio.src_attr(),type=audio.mimetype, autoplay=audio.autoplay_attr())
# HTML(new_html(audio))
def anim_to_html(anim,fps,uniq_id):
    if not hasattr(anim, '_encoded_video'):
        with NamedTemporaryFile(suffix='.mp4') as f:
            anim.save(f.name, fps=fps, extra_args=['-vcodec', 'libx264'])
            video = open(f.name, "rb").read()
        anim._encoded_video = video.encode("base64")
    
    return VIDEO_TAG.format(anim._encoded_video,uniq_id)

def display_animation1(anim,fps):
    plt.close(anim._fig)
    return HTML(anim_to_html(anim,fps))
def controls(uniq_id):
    return CONTROLS_TAG % (uniq_id, uniq_id)

def display_animation_with_sound(anim,fps,snd,rate):
    uniq_id = ''.join(random.choice('123457890abcdefghijk') for i in range(16))

    plt.close(anim._fig)
    return HTML(
        anim_to_html(anim,fps,uniq_id) +\
        "<br><br>" +\
        new_html(ipd.Audio(snd,rate=rate),uniq_id) +\
        "<br><br>" +\
        controls(uniq_id))

def animate_sound(snd, rate, fps=13,plot=None):
    """
        Animates a bar moving accross the plot of the sound (or of plot, if given), while playing the music.
        snd: the sound to play
        rate: the sample rate of snd
        fps: the frame rate of the animation. Higher frame rates are smoother and slower to generate.
        plot: optionally, a different thing than the audio for the bar to scroll across.
    """
    if plot is None:
        plot = snd
    fig = plt.figure()
    ax = plt.axes(xlim=(0, len(snd)), ylim=(-.5, .5))
    line, = ax.plot([], [], lw=2)
    plt.plot(snd)
    def init():
        line.set_data([], [])
        return line,
    
    # animation function.  This is called sequentially
    def animate(i):
        x = (i*rate*1./fps,i*rate*1./fps)
        y = (-1,1)
        line.set_data(x, y)
        return line,
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=int(math.ceil(len(snd)*1./rate*fps)), interval=1000/fps, blit=False)


    return display_animation_with_sound(anim,fps,snd,rate)