module.exports = {
    extends: [
        "eslint:recommended",
        "plugin:vue/base"
    ],
    parser: "vue-eslint-parser",
    parserOptions: {
        parser: "babel-eslint",
        sourceType: "module"
    },
    env: {
        es6: true,
        browser: true,
        node: true
    }
}