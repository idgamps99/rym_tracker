// listen to tabs being created
// if tab.url contains rateyourmusic
// get local storage count: with default value of 0
// increment count by 1
// set new count in stoage

// THEN
// make sure that each visit is unique by checking other open tabs

async function getUniqueVisits() {
  const defaultVal = 0
  const result = await chrome.storage.local.get("uniqueVisitsCount")
  if (result.uniqueVisitsCount !== undefined) {
    return result.uniqueVisitsCount
  } else {
    return defaultVal
  }
}

async function setUniqueVisits(visitsCount) {
  await chrome.storage.local.set({ "uniqueVisitsCount": visitsCount})
}

chrome.tabs.onUpdated.addListener(async (tabId, tab) => {
  if (tab.url && tab.url.includes("rateyourmusic.com")) {
    // get local storage
    // increment by 1
    // set new counter in storage
    let uniqueVisitsCount = await getUniqueVisits()
    uniqueVisitsCount++
    await setUniqueVisits(uniqueVisitsCount)
  }
})


