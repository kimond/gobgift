var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CleanWebpackPlugin = require('clean-webpack-plugin');

var dist_dir = '/frontend/dist';

var dev_server_addr = 'localhost';
var dev_server_port = 8080;

module.exports = {
    entry: {
        default: ['./frontend/src/main.js'],
    },
    output: {
        path: path.resolve(__dirname, '.' + dist_dir + '/'),
        filename: '[name]-[hash].js',
        publicPath: '/static/dist/',
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)(\?\S*)?$/,
                loader: 'file-loader'
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]?[hash]'
                }
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
        }
    },
    devServer: {
        historyApiFallback: true,
        noInfo: true,
        headers: {"Access-Control-Allow-Origin": "*"}
    },
    performance: {
        hints: false
    },
    devtool: '#eval-source-map'
};

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map';
    // http://vue-loader.vuejs.org/en/workflow/production.html
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            sourceMap: true,
            compress: {
                warnings: false
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true
        }),
        new BundleTracker({
            filename: './webpack-stats-prod.json'
        }),
        new CleanWebpackPlugin(['dist'], {
            root: path.resolve(__dirname, './frontend/'),
            verbose: true
        })
    ])
}
else if (process.env.NODE_ENV === 'development') {
    Object.values(module.exports.entry).map((entry) => {
        entry.push('webpack-dev-server/client?http://' + dev_server_addr + ':' + dev_server_port)
    });
    Object.values(module.exports.entry).map((entry) => {
        entry.push('webpack/hot/only-dev-server')
    });
    module.exports.output['publicPath'] = 'http://' + dev_server_addr + ':' + dev_server_port + dist_dir + '/';
    module.exports.plugins.push(new webpack.HotModuleReplacementPlugin());
    module.exports.plugins.push(new webpack.NoEmitOnErrorsPlugin()); // don't reload if there is an error
}
