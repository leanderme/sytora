import React from 'react'
import ReactDOM from 'react-dom'

import Header from './header/Header.jsx'

export default class MainWindow extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            username: 'test'
        }
    }

    render() {
        return (
            <div>
                <Header username={this.state.username} />
            </div>
        )
    }
}