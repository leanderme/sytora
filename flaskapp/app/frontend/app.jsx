import React from 'react';
import { render } from 'react-dom';
// import Index from './pages/index.jsx';
import Landing from './pages/landing.jsx';
import Search from './pages/list.jsx';
import './i18n';
import { BrowserRouter } from 'react-router-dom'
import { Switch, Route, Link } from 'react-router-dom';


const Index = () => {
	return (
		<div>
			<h2>Home</h2>
		</div>
	);
};

const About = () => <h2>About</h2>;
const Users = () => <h2>Users</h2>;


const Header = () => (
  <header>
  </header>
)

const App = () => (
  <div>
    <Main />
  </div>
)


const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={Landing}/>
      <Route path='/search' component={Search}/>
      <Route path='/users' component={Users}/>
    </Switch>
  </main>
)



render((
  <BrowserRouter>
    <App />
  </BrowserRouter>
), document.getElementById('root'))