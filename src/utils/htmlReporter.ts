import reporter from 'cucumber-html-reporter';

const options = {
        theme: "bootstrap" as "bootstrap",
        jsonFile: 'cucumber-report.json',
        output: 'reports/cucumber_report.html',
        reportSuiteAsScenarios: true,
        scenarioTimestamp: true,
        launchReport: true,
        metadata: {
            "App Version":"0.3.2",
            "Test Environment": "STAGING",
            "Browser": "Chrome",
            "Platform": "Windows 11"
        }
    };

    reporter.generate(options);
    