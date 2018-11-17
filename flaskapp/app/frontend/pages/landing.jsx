/* eslint-disable flowtype/require-valid-file-annotation */
import axios from 'axios';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Button from 'material-ui/Button';
import classNames from 'classnames';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import withRoot from '../components/withRoot.jsx';
import VirtualizedSelect from 'react-virtualized-select';
import { Creatable } from 'react-select'
import 'react-select/dist/react-select.css';
import 'react-virtualized/styles.css';
import 'react-virtualized-select/styles.css';
import orange from 'material-ui/colors/orange';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import Chip from 'material-ui/Chip';
import Done from 'material-ui-icons/Done';
import Snackbar from 'material-ui/Snackbar';
import IconButton from 'material-ui/IconButton';
import CloseIcon from 'material-ui-icons/Close';
import List, { ListItem, ListItemText } from 'material-ui/List';
import Search from 'material-ui-icons/Search';
import Avatar from 'material-ui/Avatar';
import * as Emojione from 'react-emojione';
import Select from 'react-select';
import ClapButton from '../components/Clap.jsx';
import Pray_tone1 from '../emoji/Pray_tone1';
import FlagDE from '../emoji/Flag_de';
import FlagEN from '../emoji/Flag_us';

import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  withMobileDialog,
} from 'material-ui/Dialog';

import { I18nextProvider, NamespacesConsumer, Trans, withNamespaces } from 'react-i18next';
import i18n from '../i18n';

import { withRouter } from "react-router-dom";


import { createMuiTheme, MuiThemeProvider } from 'material-ui/styles';

const theme1 = createMuiTheme({
  palette: {
    primary: {
      main: '#6078ff',
    }
  },
});


 
const blue = {
  50: '#e3f2fd',
  100: '#bbdefb',
  200: '#90caf9',
  300: '#64b5f6',
  400: '#42a5f5',
  500: '#0069ff',
  600: '#1e88e5',
  700: '#1976d2',
  800: '#1565c0',
  900: '#0d47a1',
  A100: '#82b1ff',
  A200: '#448aff',
  A400: '#2979ff',
  A700: '#2962ff',
  contrastDefaultColor: 'light',
};

const DATA = require('../data/labels');
const DISEASES = require('../data/diseases');

const getOptions = (input) => {
  return fetch("http://localhost:5001" + `api/search?label=${input}`)
    .then((response) => {
      return response.json();
    }).then((json) => {
      return { options: json };
    });
}

const styles = theme => ({
  title: {
    color: theme.palette.text.secondary,
    '&:hover': {
      color: theme.palette.primary[500],
    },
  },
  // https://github.com/philipwalton/flexbugs#3-min-height-on-a-flex-container-wont-apply-to-its-flex-items
  toolbarIe11: {
    display: 'flex',
  },
  toolbar: {
    flexGrow: 1,
    flexDirection: 'column',
    alignItems: 'flex-start',
    justifyContent: 'center',
  },
  root: {
    width: '100%',
    backgroundImage: 'linear-gradient(19deg, #21D4FD 0%, #B721FF 100%)'
  },
  chip: {
    margin: theme.spacing.unit,
  },
  row: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  flex: {
    flex: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
  appFrame: {
    position: 'relative',
    width: '100%',
    height: '100%',
    minHeight: '100vh',
    alignItems: 'stretch',
    overflowX: 'hidden'
  },
  footer: {
    display: 'block',
  },
  noBullets: {
    listStyle: 'none',
    paddingLeft: '10px'
  },
  appBar: {
    position: 'absolute',
    boxShadow: 'none',
    background: 'white',
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 20,
  },
  hide: {
    display: 'none',
  },
  content: {
    width: '100%',
    flexGrow: 1,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    height: 'calc(100% - 56px)',
    marginTop: 56,
    [theme.breakpoints.up('sm')]: {
      content: {
        height: 'calc(100% - 64px)',
        marginTop: 64,
      },
    },
  },
  contentShift: {
    marginLeft: 0,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  colorChip: {
    background: blue[100]
  },
  feedbackChip: {
    border: "1px dashed"
  },
  welcomeBlock: {
    backgroundImage: "url('./static/imgs/bg_1.svg')"
  },
  smallSVG: {
    height: 18,
    width: 18
  }
});


const instructTop = (props) => {
  const { symptoms } = props;
  return (<Trans i18nKey='instructFeedbackTop'>Hello {{symptoms}}</Trans>);
}

const InstructTopWithHoc = withNamespaces()(instructTop);

const instructList = (props) => {
  const { disease } = props;
  return (
    <Trans i18nKey='instructFeedbackList'>
      Welche Symptome passen zu {{disease}}? Bitte Symptome anklicken, um Feedback zu geben.
    </Trans>
  );
}

const InstructListWithHoc = withNamespaces()(instructList);


class Index extends Component {
  state = {
    open: false,
    value: [],
    results: [],
    selected: [],
    drawer: false,
    feedbackSelected: [],
    message: "",
    clapped: [],
    dialog: false,
    newDisease: {},
    newDiseaseSymptoms: [],
    language: "en"
  };

  changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    this.setState({ language: lng });
  }

  findSuggestions = (symptom) => {
    axios.post("http://localhost:5001" + 'api/sySuggest', { "symptom": symptom[0].value })
      .then((result) => {
        console.log(result);

        this.setState({
          'message': result.data.join(', ') + ' passen auch noch zu ' + symptom[0].label,
          'open': true
        });
      });
  }

  // on change of the main search input.
  onChange = (value) => {
    console.log(value);

  
    this.setState({ value: value });
  };

  onSubmit = (e) => {
    e.preventDefault();
    const { value } = this.state;
    if (value.length == 0) {
      return
    }

    let vals = value.map((v) => {
      return v.value
    });

    console.log(value);

    this.props.history.push({
      pathname: "/search/",
      search: "?sy=" + vals.join(','),
      state: { value: value },
    });

    /*
    history.push({
      pathname: "/search/",
      search: "?sy=" + vals.join(','),
      state: { some: "state" }
    });
    */
    /*
    axios.post("http://localhost:5001" + 'api/predict?lang='+this.state.language, { "symptoms": vals })
      .then((result) => {
        //access the results here....
        console.log(result);
        this.setState({ 'results': result.data });
      });
    */
  }


  render() {
    const classes = this.props.classes;
    let symptoms = this.state.value.map((v) => {return v.label}).join(', ');
    return (
      <MuiThemeProvider theme={theme1}>
        <I18nextProvider i18n={i18n}>
          <div className={this.props.classes.root}>
            <div className={classes.appFrame}>
              <main className={classNames(classes.content)}>
                  <div>
                    <section style={{background: "transparent"}}>
                      <div className="container">
                        <div className="row justify-content-center">
                          <div className="col-12 col-md-10 col-lg-8">
                            <div className="mt-4">
                              <div className="text-white text-center">
                                <NamespacesConsumer>
                                  {
                                    t => <h1>{t('homeTitle')}</h1>
                                  }
                                </NamespacesConsumer>
                                <div className="iphonehide">
                                  <p className="text-h3">
                                    <NamespacesConsumer>
                                      {
                                        t => (t('introTextOne'))
                                      }
                                    </NamespacesConsumer>
                                  </p>
                                  <p className="mt-4 pb-4">
                                   <NamespacesConsumer>
                                      {
                                        t => (t('introTextTwo'))
                                      }
                                    </NamespacesConsumer>
                                  </p>
                                </div>
                              </div>
                              <div className="landing-box">
                                  <Grid container spacing={24}>
                                    <Grid item xs={10}>
                                      <NamespacesConsumer>
                                        {
                                          t => (
                                            <VirtualizedSelect
                                              ref="symptomSelect"
                                              name="form-field-name"
                                              options={DATA.LABELS}
                                              onChange={this.onChange}
                                              value={this.state.value}
                                              multi
                                              searchable
                                              placeholder={t('searchPlaceholder')}
                                              searchPromptText={t('searchPlaceholder')}
                                              autofocus={true}
                                              autosize={true}
                                              required={true}
                                            />
                                          )
                                        }
                                      </NamespacesConsumer>
                                    </Grid>
                                    <Grid item xs={2}>
                                      <div className="pl-2">
                                      <Button variant="fab" variant="raised" size="small" color="primary" onClick={this.onSubmit}>
                                        <Search className={this.props.classes.smallSVG}/>
                                      </Button>
                                      </div>
                                    </Grid>
                                  </Grid>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </section>
                  </div>
                  
                <footer className={classes.footer} id="footerFixed">
                  <div className="container">
                    <Grid container spacing={8}>
                      <Grid item xs>
                       <a href="./legal">Legal</a>
                      </Grid>
                      <Grid item xs={4}>
                        Change language
                        <ul className={classes.noBullets}>
                          <li><a onClick={() => this.changeLanguage('de')}> <FlagDE width={20} height={20}/> de</a></li>
                          <li><a onClick={() => this.changeLanguage('en')}> <FlagEN width={20} height={20}/> en</a></li>
                        </ul>
                      </Grid>
                      <Grid item xs={4}>
                        Created with <strike>love</strike> a keyboard
                      </Grid>
                    </Grid>
                  </div>
                </footer>


              </main>
            </div>
          </div>
        </I18nextProvider>
      </MuiThemeProvider>
    );
  }
};


Index.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRoot(withRouter(withStyles(styles)(Index)));