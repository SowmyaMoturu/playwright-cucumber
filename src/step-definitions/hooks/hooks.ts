
import { Before, After, BeforeAll, AfterAll, Status, setDefaultTimeout, AfterStep } from '@cucumber/cucumber';
import { ensureDir } from 'fs-extra';
import { Browser, chromium, webkit, request, devices } from 'playwright';
import { browserOptions } from '../../setup/config';
import { ScenarioWorld } from '../../setup/world';
import { BasePage } from '../../pages/basepage';

const tracesDir = 'traces';

const browserType: string = process.env.browserType ?? 'chromium';
const videoRecording = process.env.videoRecording === 'true';
const take_screenshot = process.env.takeScreenshot === 'true';
let browser: Browser;

setDefaultTimeout(60 * 1000);

const device = browserType === 'webkit' ? devices['Desktop Safari'] : devices['Desktop Chrome'];
const headless = process.env.CI === 'true';

BeforeAll(async function () {
  switch (browserType) {

    case 'webkit':
      browser = await webkit.launch({ ...browserOptions, headless :headless});
      break;
    case 'msedge':
      browser = await chromium.launch({ ...browserOptions, channel: 'msedge' , headless :headless});
      break;
    case 'chrome':
      browser = await chromium.launch({ ...browserOptions, channel: 'chrome' , headless :headless});
      break;
    default:
        browser = await chromium.launch({ ...browserOptions, channel: 'chrome', headless :headless });
  }
 
  await ensureDir(tracesDir);
});

Before(async function (this: ScenarioWorld, { pickle }) {
  this.baseUrl = this.parameters?.baseUrl
  this.apiUrl = this.parameters?.apiUrl
  this.startTime = new Date();
  this.testName = pickle.name.replace(/\W/g, '-');

  const { viewport } = device;

  this.context = await browser.newContext({
    acceptDownloads: true,
    recordVideo: videoRecording ? { dir: 'recordings' } : undefined,
    viewport,
    baseURL: this.parameters?.baseUrl,
    ignoreHTTPSErrors: true
  });

  this.request = await request.newContext({
    ignoreHTTPSErrors: true,
    baseURL: this.parameters?.apiURL
  });

  await this.context.tracing.start({ screenshots: true, snapshots: true });
  this.page = await this.context.newPage();

  BasePage.page = this.page;

  this.feature = pickle;
});

AfterStep(async function (this: ScenarioWorld) {
  if (take_screenshot) {
    this.attach(`Scenario: ${this.feature?.name || 'Unknown Scenario'}`);
    const screenshot = await this.page?.screenshot({fullPage:true});
    if (screenshot) {
      this.attach(screenshot, 'image/png');
    }
  }
});

After(async function (this: ScenarioWorld, { result }) {
  if (result) {
    this.attach(`Status: ${result?.status}. Duration:${result.duration?.seconds}s`);

    if (result.status !== Status.PASSED) {
      const image = await this.page?.screenshot();
      
      if (image) {
        this.attach(image, 'image/png');
      }
      await this.context?.tracing.stop({
        path: `${tracesDir}/${this.testName}.zip`
      });
    }
  }
  await this.page?.close();
  await this.page?.video()?.saveAs(`recordings/${this.testName}.mp4`)
  await this.context?.close();
});

AfterAll(async function () {
  await browser.close();
});