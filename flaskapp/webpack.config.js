const webpack = require('webpack');

module.exports = {
    entry: [
        './app/frontend/app.jsx'
    ],
    module: {
        rules: [
            {
                test: /.jsx?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel-loader',
                query: {
                    presets: ["es2015", "stage-0", "react"]
                }
            },
            {
                test: /\.css$/,
                use: [ 'style-loader', 'css-loader' ]
            },
            {
              test: /\.svg$/,
              loaders: [
                'babel-loader',
                {
                  loader: 'react-svg-loader',
                  query: {
                    jsx: true
                  }
                },
              ]
            },
            {
                test   : /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/,
                loader : 'file-loader'
            }
        ]
    },
    output: {
        filename: 'bundle.js',
        path: __dirname + '/app/backend/static'
    },
    plugins: (() => {
    // overload -p flag in $ webpack -p
    // for more info on $ webpack -p see: https://webpack.github.io/docs/cli.html#production-shortcut-p
    if (process.argv.indexOf('-p') !== -1) {
      return [
        new webpack.DefinePlugin({
          'process.env': {
            NODE_ENV: JSON.stringify('production'),
            REACT_APP_ENDPOINT: process.env.REACT_APP_ENDPOINT
          },
        }),

        // note that webpack's -p shortcut runs the UglifyJsPlugin (https://github.com/webpack/docs/wiki/optimization)
        // but for some reason leaves in one multiline comment while removing the rest,
        // so have to set comments: false here to remove all the comments
        new webpack.optimize.UglifyJsPlugin({
          output: {
            comments: false,
          },
        }),
      ];
    }
    return [
      new webpack.DefinePlugin({
        'process.env': {
          REACT_APP_ENDPOINT: JSON.stringify(process.env.REACT_APP_ENDPOINT)
        },
      }),
    ];
  })(),
}