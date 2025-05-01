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

async function recordVisit(isUnique) {
  const url = "http://127.0.0.1:8000/visits/record"
  const body = {"isUnique": isUnique}

  console.log("RECORDING VISIT!!!!")
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
      },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    console.log("RESPONSE:", response)

  } catch (error) {
    console.log("Couldn't record visit:", error)
  }
}

chrome.tabs.onUpdated.addListener(async (tabId, tab) => {
  console.log("tabs updated")

  if (tab.url && tab.url.includes("rateyourmusic.com")) {
    const isUniqueVisit = await checkIfUniqueVisit()
    console.log("Is Unique?", isUniqueVisit)
    if (isUniqueVisit) await incrementUniqueVisit()
    await recordVisit(isUniqueVisit)
  }

  await setOpenedTabsUrls()
})

