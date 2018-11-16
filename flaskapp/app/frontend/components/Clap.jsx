import React, { Component } from 'react';
import ReactDOM from 'react-dom'
import mojs from 'mo-js'
import classNames from 'classnames';

function updateNumberOfClaps() {
  numberOfClaps < 50 ? numberOfClaps++ : null
  clapCount.innerHTML = "+" + numberOfClaps
  clapTotalCount.innerHTML = initialNumberOfClaps + numberOfClaps
  console.log(numberOfClaps)
}

function generateRandomNumber(min, max) {
  return Math.floor(Math.random()*(max-min+1)+min);
}

class Clap extends Component {
    componentDidMount() {
      this._burst = new mojs.Burst({
        left: 0, top: 0,
        radius:   { 0: 100 },
        count:    5,
        children: {
          shape:        'circle',
          radius:       15,
          fill:       [ 'deeppink', 'cyan', 'yellow' ],
          strokeWidth:  5,
          duration:     2000
        },
        timeline() {
          onComplete: ()=> { this.props.onComplete && this.props.onComplete(); }
        }
      });

    }

    playAtMouseCursor = (e) => {

      const coords = { x: e.pageX, y: e.pageY };
      this._burst
        .tune(coords)
        .setSpeed(3)
        .replay();
    }

    render() {
        return (
          <div></div>
        )
    }
}

export default class ClapButton extends Component {
   state = {
    isPlay: true,
    checked: false
  };
  _play = () => { this.setState({ isPlay: true, checked: true }); };

  _resetPlay = () => { this.setState({ isPlay: false }); };

  _handleClick = (e) => {
    this.setState({ checked: true });
    this.refs.child.playAtMouseCursor(e);
    this.props.onClick();
  }

  render() {
    return (
      <div>
        <button id={"clap"} className={"clap"} onClick={this._handleClick}>
          <span>
            <svg id="clap--icon" xmlns="http://www.w3.org/2000/svg" viewBox="-549 338 100.1 125">
              <path d="M-471.2 366.8c1.2 1.1 1.9 2.6 2.3 4.1.4-.3.8-.5 1.2-.7 1-1.9.7-4.3-1-5.9-2-1.9-5.2-1.9-7.2.1l-.2.2c1.8.1 3.6.9 4.9 2.2zm-28.8 14c.4.9.7 1.9.8 3.1l16.5-16.9c.6-.6 1.4-1.1 2.1-1.5 1-1.9.7-4.4-.9-6-2-1.9-5.2-1.9-7.2.1l-15.5 15.9c2.3 2.2 3.1 3 4.2 5.3zm-38.9 39.7c-.1-8.9 3.2-17.2 9.4-23.6l18.6-19c.7-2 .5-4.1-.1-5.3-.8-1.8-1.3-2.3-3.6-4.5l-20.9 21.4c-10.6 10.8-11.2 27.6-2.3 39.3-.6-2.6-1-5.4-1.1-8.3z"/>
              <path d="M-527.2 399.1l20.9-21.4c2.2 2.2 2.7 2.6 3.5 4.5.8 1.8 1 5.4-1.6 8l-11.8 12.2c-.5.5-.4 1.2 0 1.7.5.5 1.2.5 1.7 0l34-35c1.9-2 5.2-2.1 7.2-.1 2 1.9 2 5.2.1 7.2l-24.7 25.3c-.5.5-.4 1.2 0 1.7.5.5 1.2.5 1.7 0l28.5-29.3c2-2 5.2-2 7.1-.1 2 1.9 2 5.1.1 7.1l-28.5 29.3c-.5.5-.4 1.2 0 1.7.5.5 1.2.4 1.7 0l24.7-25.3c1.9-2 5.1-2.1 7.1-.1 2 1.9 2 5.2.1 7.2l-24.7 25.3c-.5.5-.4 1.2 0 1.7.5.5 1.2.5 1.7 0l14.6-15c2-2 5.2-2 7.2-.1 2 2 2.1 5.2.1 7.2l-27.6 28.4c-11.6 11.9-30.6 12.2-42.5.6-12-11.7-12.2-30.8-.6-42.7m18.1-48.4l-.7 4.9-2.2-4.4m7.6.9l-3.7 3.4 1.2-4.8m5.5 4.7l-4.8 1.6 3.1-3.9"/>
            </svg>
          </span>
        </button>
        <Clap ref="child" isPlay={this.state.isPlay} onComplete={this._resetPlay}/>
      </div>
    );
  }
}

/*====== TODO ==========
1. Bug fix. The button shouldn't
scale up before being clicked (fixed)
2. Shadow should NOT fire hover
animation in succession.
Some sort of delay is delay.
3. Hover animation should be
absent upon click
4. Handle onpress event on the button
5. Dynamically change burst angle
everytime button is clicked
=========================*/


