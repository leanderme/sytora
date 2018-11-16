import i18n from 'i18next';
import { reactI18nextModule } from 'react-i18next';


const resources = {
  en: {
    translation: {
      "homeTitle": "Smart Symptom Search",
      "instructFeedbackTop": "Please click on the clap-icon on the left side of the disease entry, which matches the most your search query.",
      "instructFeedbackList": "Which symptoms match {{disease}}? Please click on the symptoms below to give feedback.",
      "clapLabel": "Looking for this?",
      "missingSy": "Something missing?",
      "giveFeedbackTitle": "Give Feedback",
      "giveFeedbackPlaceholder": "Something missing? Type in here",
      "diseaseMissing": "Disease not in list?",
      "searchPlaceholder": "Type in symptoms to search",
      "addDisease": "Add a Disease",
      "cancel": "Cancel",
      "symptomsFor": "Symptoms for ",
      "introTextOne": "This project uses Machine Learning to generate differential diagnoses for given symptoms. You can improve accuracy by clicking on symptoms you would have expected for a disease.",
      "introTextTwo": "We've already collected (by hand) ~ 600 diseases and ~ 1500 Symptoms. Please help by using this site. All is available on GitHub under CC 4.0",
      
    }
  },
  de: {
    translation: {
      "homeTitle": "Intelligente Symptomsuche",
      "instructFeedbackTop": "Bitte wähle in der Liste aus, welche Krankheit du zu den Symptomen gesucht hast, indem du auf das Clap-Icon klickst. Falls Symptome zu einer Krankheit nicht gelistet sind, kannst du diese unter Fehlt etwas hinzufügen.",
      "instructFeedbackList": "Welche Symptome passen zu {{disease}}? Bitte Symptome anklicken, um Feedback zu geben.",
      "clapLabel": "Das gesucht?",
      "missingSy": "Fehlt etwas?",
      "giveFeedbackTitle": "Feedback geben",
      "giveFeedbackPlaceholder": "Fehlt etwas? Hier eingeben",
      "diseaseMissing": "Erkrankung nicht dabei?",
      "searchPlaceholder": "Hier Symptome zur Suche eingeben",
      "addDisease": "Erkrankung hinzufügen",
      "cancel": "Abbrechen",
      "symptomsFor": "Symptome für ",
      "introTextOne": "Dieses Projekt nutzt Machine-Learning, um Differentialdiagnosen herauszuarbeiten. Du kannst die Qualität durch Feedback verbessern, indem du anklickst, welche Diagnose du bei den eingegebenen Symptomen erwartet hättest.",
      "introTextTwo": "Wir haben bereits ~ 600 Erkrankuungen und 1500 gesammelt. Hilf' mit und verbessere die Suche! Alle Daten sind auf GitHub verfügbar unter CC 4.0",
    }
  }
};


i18n
  // pass the i18n instance to the react-i18next components.
  // Alternative use the I18nextProvider: https://react.i18next.com/components/i18nextprovider
  .use(reactI18nextModule)
  // init i18next
  // for all options read: https://www.i18next.com/overview/configuration-options
  .init({
    resources,
    lng: "de",
    fallbackLng: 'en',
    debug: true,
    saveMissing: false,
    interpolation: {
      escapeValue: false, // not needed for react as it escapes by default
    },

    // special options for react-i18next
    // learn more: https://react.i18next.com/components/i18next-instance
    react: {
      wait: true
    }
  });


export default i18n;