const options = {
    require: ['src/step-definitions/**/*.ts'],
    paths: ['src/features/**/*.feature'],
    format: ['json:cucumber-report.json'],
    requireModule: ['ts-node/register'],
    parallel: 1
}

const worldParameters = {
    baseUrl: "https://magento.softwaretestingboard.com/",
    apiUrl: ""
}


module.exports = {
    default: {
        ...options,
        worldParameters: {
            ...worldParameters
        }
    },
    sit:{
        ...options,
        worldParameters: {
            ...worldParameters,
            env: "sit"
        }
    },
    uat: {
        ...options,
        worldParameters: {
             baseUrl: "https://magento.softwaretestingboarduat.com/",
             apiUrl: "uat api url",
             env: "uat"
        }
    },
    smoke:{
        ...options,
        tags: "@smoke",
        worldParameters: {
            ...worldParameters
        }
    }
};
