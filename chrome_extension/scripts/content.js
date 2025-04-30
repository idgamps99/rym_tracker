console.log("hello, rym")

chrome.storage.local.get(["uniqueVisitsCount"]).then((result) => {
  console.log("Value is " + result.uniqueVisitsCount)
})
