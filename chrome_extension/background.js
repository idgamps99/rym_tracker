import { API_KEY } from './config.js'

async function getAllOpenTabs() {
  return await chrome.tabs.query({})
}

async function setOpenedTabsUrls() {
  const tabs = await getAllOpenTabs()
  const urls = tabs.map((tab) => tab.url)
  await chrome.storage.local.set({ "urls": urls })
}

async function setUniqueVisits(visitsCount) {
  await chrome.storage.local.set({ "uniqueVisitsCount": visitsCount })
}

async function getUniqueVisits() {
  const result = await chrome.storage.local.get({"uniqueVisitsCount": 0 })
  return result.uniqueVisitsCount
}

async function incrementUniqueVisit() {
  console.log("Let's increment this shit")
  let uniqueVisitsCount = await getUniqueVisits()
  uniqueVisitsCount++
  await setUniqueVisits(uniqueVisitsCount)
}

async function getOpenedTabsUrls() {
  const res = await chrome.storage.local.get({ "urls": [] })
  return res.urls
}

async function checkIfUniqueVisit() {
  const urls = await getOpenedTabsUrls()
  for(let i = 0; i < urls.length; i++) {
    if (urls[i].includes("rateyourmusic.com")) {
      console.log(urls[i])
      return false
    }
  }
  return true
}

chrome.tabs.onUpdated.addListener(async (tabId, tab) => {
  console.log("tabs updated")

  if (tab.url && tab.url.includes("rateyourmusic.com")) {
    const isUniqueVisit = await checkIfUniqueVisit()
    console.log("Is Unique?", isUniqueVisit)
    if (isUniqueVisit) await incrementUniqueVisit()
  }

  await setOpenedTabsUrls()
})
