import {
    Player, LoadingSpinner, ReplayControl, ForwardControl, CurrentTimeDisplay,
    VolumeMenuButton, ControlBar, BigPlayButton, PlayToggle
} from "video-react";
import '../../../node_modules/video-react/dist/video-react.css'

const VideoPlayer = ({id ,src, preview}) => {
    return (
        <Player src={src} poster={preview} fluid={true}>
            <BigPlayButton position="center"/>
            <ControlBar autoHide={true}>
                <PlayToggle/>
                <LoadingSpinner/>
                <ReplayControl seconds={10} order={1.1}/>
                <ForwardControl seconds={10} order={1.2}/>
                <CurrentTimeDisplay order={1.3}/>
                <VolumeMenuButton horizontal/>
                </ControlBar>
        </Player>
    );
};

export default VideoPlayer;