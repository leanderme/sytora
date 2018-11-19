/* eslint-disable flowtype/require-valid-file-annotation */
import axios from 'axios';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Button from 'material-ui/Button';
import classNames from 'classnames';
import Divider from 'material-ui/Divider';
import Grid from 'material-ui/Grid';
import Typography from 'material-ui/Typography';
//import { createMuiTheme, MuiThemeProvider, withStyles } from 'material-ui/styles';
import { MuiThemeProvider, createMuiTheme, withStyles} from '@material-ui/core/styles';

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

import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Collapse from '@material-ui/core/Collapse';
import red from '@material-ui/core/colors/red';
import FavoriteIcon from '@material-ui/icons/Favorite';
import ShareIcon from '@material-ui/icons/Share';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import MoreVertIcon from '@material-ui/icons/MoreVert';


import * as Emojione from 'react-emojione';
import Select from 'react-select';
import ClapButton from '../components/Clap.jsx';
import Pray_tone1 from '../emoji/Pray_tone1';
import FlagDE from '../emoji/Flag_de';
import FlagEN from '../emoji/Flag_us';
import { withRouter } from "react-router-dom";

import Dialog, {
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  withMobileDialog,
} from 'material-ui/Dialog';

import { I18nextProvider, NamespacesConsumer, Trans, withNamespaces } from 'react-i18next';
import i18n from '../i18n';

var URLSearchParams = require('url-search-params');

const fetcher = axios.create({
  baseURL: process.env.REACT_APP_ENDPOINT,
  headers: {
    'Content-Type': 'application/json'
  }
});

const fetchPredictions = (lng, symptoms) => {
  return fetcher.post('/api/predict?lang='+lng, { "symptoms": symptoms }).then(res => {
    return res.data;
  });
};


const fetchSuggestions = (symptom) => {
  return fetcher.post('/api/sySuggest', { "symptom": symptom[symptom.length - 1].value }).then(res => {
    return res.data;
  });
};

const postFeedback = (selected) => {
  return fetcher.post('api/feedback', { "feedback": selected }).then(res => {
    return res.data;
  });
};


const availableLng = ['en', 'de'];
let DATA = {};

availableLng.forEach((lat, index) => {
    DATA[lat] = require('../data/' + lat + '_Labels');
});

const DISEASES = require('../data/diseases');

const getOptions = (input) => {
  return fetch(window.location.href + `api/search?label=${input}`)
    .then((response) => {
      return response.json();
    }).then((json) => {
      return { options: json };
    });
}

const theme1 = createMuiTheme({
  palette: {
    primary: {
      main: '#6078ff',
    }
  },
});

const styles = theme => ({
  cardListItem: {
    paddingBottom: 10
  },
  actions: {
    display: 'flex',
  },
  expand: {
    transform: 'rotate(0deg)',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
    marginLeft: 'auto',
    [theme.breakpoints.up('sm')]: {
      marginRight: -8,
    },
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
  toolbar: {
    flexGrow: 1,
    flexDirection: 'column',
    alignItems: 'flex-start',
    justifyContent: 'center',
  },
  root: {
    backgroundImage: 'linear-gradient(19deg, #21D4FD 0%, #B721FF 100%)'
  },
  chip: {
    margin: 4,
  },
  row: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  flex: {
    flex: 1,
  },
  appFrame: {
    position: 'relative',
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
    position: 'relative',
    background: '#ffffff',
  },
  hide: {
    display: 'none',
  },
  colorChip: {
    background: '#bbdefb'
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
  },
  inlineBlock: {
    display: 'inline-block'
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  sy: {
    color: 'inherit',
  },
  highlight: {
    color: '#6078ff'
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


const hasDisease = (arrOfObj, disease, checkOnly) => {
  var found = false;
  let index;
  for (var i = 0; i < arrOfObj.length; i++) {
      if (arrOfObj[i]['disease'] == disease) {
          found = true;
          index = i
          break;
      }
  }
  if (checkOnly)
    return found;
  return found, index;
}

class Index extends Component {

  constructor(props) {
    super(props);

    const { location = {'state': {'value' : [] } } } = props

    this.state = {
      open: false,
      value: location, //value holds the search query (arr of objs)
      results: [], // result holds the predictions
      selected: [], // selected holds the current symptom selection
      feedbackSelected: [],
      message: "",
      clapped: [],
      dialog: false,
      newDisease: {},
      newDiseaseSymptoms: [],
      language: "en",
      symptomOptions: DATA['en']['en' + 'LABELS'],
      suggestions: [], // suggestion holds similar symptoms (arr of obj)
      expanded: []
    }
  }


  handleExpandClick = (panel) => {
    let newStateExpanded = this.state.expanded;
    let index = newStateExpanded.indexOf(panel)

    if (index === -1) {
      newStateExpanded.push(panel)
    } else {
      newStateExpanded.splice(index, 1);
    }


    this.setState({ expaned: newStateExpanded });
  };

  shouldExpandPanel = (panel) => {
    let index = this.state.expanded.indexOf(panel)
    return (index == -1 ? false : true);
  }


  changeLanguage = (lng) => {
    i18n.changeLanguage(lng);

    const { value } = this.state;

    if (value.length == 0) {
      return
    }

    let vals = [];

    if (value.every(function(i){ return typeof i === "string" })) {
      vals = value;
    } else {
      vals = value.map((v) => {
        return v.value
      });
    }

    let that = this;
    fetchPredictions(lng, vals).then(function (result){
      that.setState({
        'results': result,
        language: lng,
        symptomOptions: DATA[lng][lng + 'LABELS']
      });
    });
  }


  handleDialogOpen = () => {
    this.setState({ dialog: true });
  };

  handleDialogClose = () => {
    this.setState({ dialog: false });
  };

  handleRequestClose = () => {
    this.setState({
      open: false,
    });
  };

  handleClick = () => {
    this.setState({
      open: true,
    });
  };

  findSuggestions = (symptom) => {
    let that = this;
    fetchSuggestions(symptom).then(function (result){
      that.setState({
        'suggestions': result,
      });
    });
  }

  onChange = (value) => {
    if (value.length !== 0) {
      this.findSuggestions(value);
    }
    this.setState({ value: value });

    let vals = value.map((v) => { return v.value })

    this.props.history.push({
      pathname: "/search/",
      search: "?sy=" + vals.join(','),
    });

  };

  addToSearch = (suggestion) => {
    const { value } = this.state;

    this.setState({value:[...value, suggestion]});

    let vals = [...value, suggestion].map((v) => { return v.value })

    this.props.history.push({
      pathname: "/search/",
      search: "?sy=" + vals.join(','),
    });

    this.updateResults();
  }

  onChangeDisease = (value) => {
    if (typeof value === 'undefined' || value === null)
      value = {};
    this.setState({ newDisease: value });
  };

  onChangeDiseaseSymptoms = (value) => {
    this.setState({ newDiseaseSymptoms: value });
  };

  onChangeUMLS = (object) => {
    const { selected } = this.state;

    let index = selected.indexOf( object );
    let new_selected = selected;

    return function (feedbackSelected) {
        // perform change on this.state for name and newValue
        new_selected[index]['added'] = feedbackSelected;
        this.setState({ selected: new_selected });
    }.bind(this);
  };


  updateResults = () => {
    const { value } = this.state;

    if (value.length == 0) {
      return
    }

    let vals = [];

    if (value.every(function(i){ return typeof i === "string" })) {
      vals = value;
    } else {
      vals = value.map((v) => {
        return v.value
      });
    }

    let that = this;
    fetchPredictions(this.state.language, vals).then(function (result){
      that.setState({
        'results': result,
      });
    });
  }

  giveFeedback = (e) => {
    e.preventDefault();
    const { selected } = this.state;
    if (selected.length == 0) {
      return
    }

    let that = this;
    postFeedback(selected).then(function (result){
      console.log(result);
    });
  }

  giveFeedbackNewDisease = () => {
    const { newDisease, newDiseaseSymptoms } = this.state;
    if (newDiseaseSymptoms.length == 0 || newDisease === "") {
      this.setState({'message': 'Der Name der Krankheit darf nicht leer sein.'})
      return
    }
    let vals = newDiseaseSymptoms.map((v) => { return v.label })

    if (vals.length < 1 || vals[0] == null) {
      return;
    }

    let selected = [...this.state.selected, {
      'disease':newDisease.label,
      'symptom': vals,
      'added': []
    }];

    let that = this;
    postFeedback(selected).then(function (result){
      console.log(result);
    });
  }

  handleRequestDelete = (disease, sy)=> () => {

    const old_selected = this.state.selected;
    let new_selected;

    var found = false;
    let index;
    for (var i = 0; i < old_selected.length; i++) {
        if (old_selected[i]['disease'] == disease) {
            found = true;
            index = i
            break;
        }
    }

    if (found) {
      new_selected = old_selected;
      if (new_selected[index]['symptom'].indexOf(sy) == -1)
        new_selected[index]['symptom'] = [...new_selected[index]['symptom'], sy]
    } else {
       if (typeof sy === 'string') {
        sy = [sy]
       }
       new_selected = [...this.state.selected, {
        'disease':disease,
        'symptom': sy,
        'added': []
      }];
    }

    this.setState({
      'selected': new_selected,
      'message': sy + ' hinzugefügt.',
      'open': true
    });
  };

  removeLastAdded = () => {
    this.setState({
      'selected': [],
      'message': "",
      'open': false
    })
  };

  handleClap = (disease) => {
     const { clapped } = this.state;
     let vals = this.state.value.map((v) => { return v.label })
     if (clapped.indexOf(disease) > -1) {
      return false;
     }

     this.setState({
      "clapped": [...clapped, disease],
      'message': disease + " wird jetzt stärker bei " + vals.join(', ') + " gewichtet",
      'open': true
     });

     let selected  = [{
        'disease':disease,
        'symptom': vals,
        'added': []
      }];

    if (vals.length < 1 || vals[0] == null) {
      return;
    }

    let that = this;
    postFeedback(selected).then(function (result){
      console.log(result);
    });
  }

  getSymptomStringList(pred) {
    let symptoms = ""
    pred.sy.map((s) => {
      symptoms += s + " • "
    });
    return symptoms;
  }

  componentWillMount() {
    const { value } = this.state;
    let landingValue = [];

    const urlParams = new URLSearchParams(window.location.search);
    const syParams = urlParams.get('sy');
    let syParamsList = (syParams === '' || syParams === null ? [] : syParams.split(',') );


    let defaultValues = (!landingValue.length ? syParamsList : landingValue);

    if (!Array.isArray(value) || !value.length) {
      this.setState({ value: defaultValues });
    }

    if (defaultValues.length != 0) {

      let vals = [];

      if (defaultValues.every(function(i){ return typeof i === "string" })) {
        vals = defaultValues;
      } else {
        vals = defaultValues.map((v) => {
          return v.value
        });
      }

      let that = this;
      fetchPredictions(this.state.language, vals).then(function (result){
        that.setState({
          'results': result,
        });
      });
    }

  }

  render() {
    const classes = this.props.classes;
    let symptoms = this.state.value.map((v) => {return v.label}).join(', ');
    let transl = this.state.language === 'en' ? 'RELATED: ' : 'DAZUGEHÖRIG: ';
    let suggestionVals = this.state.suggestions.length >= 1 ? this.state.suggestions.map((v) => { return v.label }) : [];
    const { expanded } = this.state;
    const bull = <span className={classes.bullet}>•</span>;

    return (
      <MuiThemeProvider theme={theme1}>
        <I18nextProvider i18n={i18n}>
          <div className={this.props.classes.root}>
            <div className={classes.appFrame}>
               <AppBar className={classNames(classes.appBar)} color="default">
                <Toolbar>
                  <div className="container pt-2">
                    <Grid container spacing={8}>
                      <Grid item xs>
                        <NamespacesConsumer>
                          {
                            t => (
                              <VirtualizedSelect
                                ref="symptomSelect"
                                name="form-field-name"
                                options={this.state.symptomOptions}
                                onChange={this.onChange}
                                value={this.state.value}
                                multi
                                searchable
                                placeholder={t('searchPlaceholder')}
                                searchPromptText={t('searchPlaceholder')}
                                autofocus={true}
                                autosize={true}
                                required={true}
                                optionHeight={40}
                              />
                            )
                          }
                        </NamespacesConsumer>
                      </Grid>
                      <Grid item xs={1}>
                        <Button variant="raised" size="medium" color="primary" onClick={this.updateResults}>
                          <Search className={this.props.classes.smallSVG}/>
                        </Button>
                      </Grid>
                    </Grid>
                    <Grid container spacing={8}>
                      <Grid item xs={12}>
                        <div className="pt-2 pb-2">
                          {
                            this.state.suggestions.length >= 1 ?
                            <div>
                              <small>{transl}</small>
                              {this.state.suggestions.map((s, i) => {
                                if (this.state.suggestions.length - 1 === i) {
                                  return (
                                    <div className={classNames(this.props.classes.inlineBlock)} key={"div" + s.label}>
                                      <a key={s.label} onClick={() => this.addToSearch(s)} className="mr-1">{s.label}</a>
                                    </div>
                                  )
                                } else {
                                  return (
                                    <div className={classNames(this.props.classes.inlineBlock)} key={"div" + s.label}>
                                      <a key={s.label} onClick={() => this.addToSearch(s)}> {s.label} </a>
                                      <small className="mr-1" key={"small" + s.label}> • </small>
                                    </div>
                                  )
                                }
                              })}
                            </div>
                          : ''}
                        </div>
                      </Grid>
                    </Grid>
                  </div>
                </Toolbar>
              </AppBar>
              <main className={classNames(this.props.classes.content)}>
                  {this.state.results.length >= 1 ?
                  <div className="container">
                    <div>
                      <div className="mb-2 text-center pt-3">
                        <div className="card iphonehide">
                          <div className="card-body">
                            <InstructTopWithHoc symptoms={symptoms}/>
                          </div>
                        </div>
                      </div>
                      <div className="">
                         {this.state.results.map((pred) => {
                          return (
                           <div className={this.props.classes.cardListItem} key={"li" + pred.disease}>
                              <Card className={this.props.classes.card}>
                                <CardContent>
                                  <Grid
                                    justify="space-between" // Add it here :)
                                    container
                                    spacing={24}
                                  >
                                    <Grid item>
                                      <Typography variant="h5" component="h2" type="title" color="inherit">
                                        {pred.disease}
                                      </Typography>
                                    </Grid>

                                    <Grid item>
                                      <div>
                                        <small>{pred.prob + "%"}</small>
                                      </div>
                                    </Grid>
                                  </Grid>

                                  <div className={this.props.classes.row}>
                                    {pred.sy.map((s) => {
                                      let vals = this.state.value.map((v) => { return v.label })
                                      let inSearch = vals.indexOf(s) > -1;
                                      return (
                                        <small
                                          key={s}
                                          className={classNames(this.props.classes.sy, inSearch && this.props.classes.highlight)}
                                        >{s} {bull} </small>
                                      )
                                    })}
                                  </div>
                                </CardContent>
                                <CardActions className={this.props.classes.actions} disableActionSpacing>
                                  <IconButton aria-label="Looking for this?"  onClick={() => this.handleClap(pred.disease)} >
                                    <FavoriteIcon />
                                  </IconButton>
                                  <IconButton
                                    className={classNames(this.props.classes.expand, {
                                      [this.props.classes.expandOpen]: this.shouldExpandPanel(pred.disease),
                                    })}
                                    onClick={() => this.handleExpandClick(pred.disease)}
                                    aria-expanded={this.shouldExpandPanel(pred.disease)}
                                    aria-label="Show more"
                                  >
                                    <ExpandMoreIcon />
                                  </IconButton>
                                </CardActions>
                                <Collapse in={this.shouldExpandPanel(pred.disease)} timeout="auto" unmountOnExit>
                                  <CardContent>
                                    <Typography component="p">
                                      <InstructListWithHoc disease={pred.disease} />
                                    </Typography>

                                    <div className={this.props.classes.row}>
                                      {pred.sy.map((s) => {
                                        let vals = this.state.value.map((v) => { return v.label })
                                        let inSearch = vals.indexOf(s) > -1;
                                        return (
                                          <Chip
                                            label={s}
                                            key={"chip_" + s}
                                            onClick={this.handleRequestDelete(pred.disease, s)}
                                            className={classNames(this.props.classes.chip, inSearch && this.props.classes.colorChip)}
                                            avatar={
                                              <Avatar>
                                                <Done className={this.props.classes.svgIcon} />
                                              </Avatar>
                                            }
                                          />
                                        )
                                      })}
                                      <NamespacesConsumer>
                                        {
                                          t => (<Chip
                                          label={t('missingSy')}
                                          key={"missing-" + pred.disease}
                                          onClick={this.handleRequestDelete(pred.disease, this.state.value.map((v) => { return v.label }))}
                                          className={classNames(this.props.classes.chip, this.props.classes.feedbackChip)}
                                        />)
                                        }
                                      </NamespacesConsumer>
                                    </div>
                                    {
                                      this.state.selected.length >= 1 && hasDisease(this.state.selected, pred.disease, true) ?
                                        <div className="mt-2">
                                          <div className="card">
                                            <div className="card-body">
                                              <h4>
                                                <NamespacesConsumer>
                                                  {
                                                    t => (t('giveFeedbackTitle'))
                                                  }
                                                </NamespacesConsumer>
                                                <Pray_tone1 width={20} height={20}/>
                                              </h4>
                                              {this.state.selected.map(sel => (
                                                sel.disease == pred.disease ?
                                                  <div key={`section-${sel.disease}`}>
                                                    <h6>{sel.disease}</h6>
                                                    <ul>
                                                    {sel.symptom.map(item => (
                                                      <ListItem button key={`item-${item}`}>
                                                        <ListItemText primary={`${item}`} />
                                                      </ListItem>
                                                    ))}
                                                    </ul>
                                                    <NamespacesConsumer>
                                                      {
                                                        t => (
                                                          <Select.AsyncCreatable
                                                            key={'umls-picker' + sel.disease}
                                                            name={'umls-picker' + sel.disease}
                                                            value={sel.added}
                                                            multi
                                                            placeholder={t('giveFeedbackPlaceholder')}
                                                            onChange={this.onChangeUMLS(sel)}
                                                            loadOptions={getOptions}
                                                            allowCreate={true}
                                                          />
                                                        )
                                                      }
                                                    </NamespacesConsumer>
                                                    <div className="mt-2 mb-2"><Divider /></div>
                                                  </div>
                                                  : ''
                                                ))}
                                              <div className="mt-4">
                                                <Button color="primary" onClick={this.giveFeedback}>
                                                  <NamespacesConsumer>
                                                    {
                                                      t => (t('giveFeedbackTitle'))
                                                    }
                                                  </NamespacesConsumer>
                                                </Button>
                                              </div>
                                            </div>
                                          </div>
                                        </div>
                                        : ''}

                                  </CardContent>
                                </Collapse>
                              </Card>
                           </div>
                          )
                         })}

                        <div className="text-center">
                          <Button color="secondary" variant="raised" onClick={this.handleDialogOpen}>
                            <NamespacesConsumer>
                              {
                                t => (t('diseaseMissing'))
                              }
                            </NamespacesConsumer>
                          </Button>
                        </div>
                      </div>
                      <div className="pb-4"></div>
                   </div>
                  </div>
                  :
                  <div>
                    <section className="fdb-block" style={{backgroundImage: "linear-gradient(19deg, #21D4FD 0%, #B721FF 100%)"}}>
                      <div className="container">
                        <div className="row justify-content-center">
                          <div className="col-12 col-md-10 col-lg-8 text-center">
                            <div className="fdb-box">
                              <NamespacesConsumer>
                                {
                                  t => <h1>{t('homeTitle')}</h1>
                                }
                              </NamespacesConsumer>
                              <p className="text-h3">
                                <NamespacesConsumer>
                                  {
                                    t => (t('introTextOne'))
                                  }
                                </NamespacesConsumer>
                              </p>
                              <p className="mt-4">
                               <NamespacesConsumer>
                                  {
                                    t => (t('introTextTwo'))
                                  }
                                </NamespacesConsumer>
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </section>
                  </div>
                  }
                <footer className={classes.footer}>
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
          <Dialog
            open={this.state.dialog}
            onRequestClose={this.handleDialogClose}
            fullScreen={true}
          >
            <DialogTitle>
              <NamespacesConsumer>
                {
                  t => <h1>{t('addDisease')}</h1>
                }
              </NamespacesConsumer>
            </DialogTitle>
            <DialogContent>
              <DialogContentText>
                <VirtualizedSelect
                  ref="diseaseSelect"
                  name="disease-form"
                  value={this.state.newDisease}
                  options={DISEASES.DISEASES}
                  onChange={this.onChangeDisease}
                  multi={false}
                  searchable
                  placeholder="Erkrankung eingeben"
                  searchPromptText="Hier Erkrankung eingeben"
                  autosize={true}
                  required={true}
                  selectComponent={Creatable}
                />
                {Object.keys(this.state.newDisease).length !== 0 ?
                  <div className="mt-4">
                    <h4 className="mb-2">
                      <NamespacesConsumer>
                          {
                            t => (
                              t('symptomsFor')
                            )
                          }
                      </NamespacesConsumer>
                      {this.state.newDisease.value}
                    </h4>
                    <NamespacesConsumer>
                      {
                        t => (
                          <Select.AsyncCreatable
                            key={'new-disease-picker'}
                            name={'new-disease-picker'}
                            value={this.state.newDiseaseSymptoms}
                            multi
                            placeholder={t('symptomsFor') + this.state.newDisease.value}
                            onChange={this.onChangeDiseaseSymptoms}
                            loadOptions={getOptions}
                            allowCreate={true}
                          />
                        )
                      }
                    </NamespacesConsumer>
                    <div className="mt-4">
                      <Button onClick={this.giveFeedbackNewDisease} color="primary" autoFocus>
                        <NamespacesConsumer>
                          {
                            t => (t('giveFeedbackTitle'))
                          }
                        </NamespacesConsumer>
                      </Button>
                    </div>
                  </div>
                : ''}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleDialogClose} color="primary">
                <NamespacesConsumer>
                  {
                    t => (t('cancel'))
                  }
                </NamespacesConsumer>
              </Button>
              {Object.keys(this.state.newDisease).length !== 0 ?
                <Button onClick={this.giveFeedbackNewDisease} color="primary" autoFocus>
                  <NamespacesConsumer>
                    {
                      t => (t('giveFeedbackTitle'))
                    }
                  </NamespacesConsumer>
                </Button>
              : ''}
            </DialogActions>
          </Dialog>
          <Snackbar
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'left',
            }}
            open={this.state.open}
            autoHideDuration={500}
            snackbarcontentprops={{
              'aria-describedby': 'message-id',
            }}
            message={<span id="message-id">{this.state.message}</span>}
            action={[
              <IconButton
                key="close"
                aria-label="Close"
                color="inherit"
                className={classes.close}
                onClick={this.handleRequestClose}
              >
                <CloseIcon />
              </IconButton>,
            ]}
          />
        </I18nextProvider>
      </MuiThemeProvider>
    );
  }
};


Index.propTypes = {
  classes: PropTypes.object.isRequired,
};


export default withRoot(withRouter(withStyles(styles)(Index)));
