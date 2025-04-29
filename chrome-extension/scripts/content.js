// chrome.runtime.onMessage.addListener((obj, sender, response) => {
//   const { type } = obj

//   if (type === "new") {
//     console.log("HELLO MOFOS")
//   }
// })

console.log("hello, rym")

// chrome.storage.local.get(["uniqueVisitsCount"], (result) => {
//   console.log("result: ", result.uniqueVisitsCount)
// })
chrome.storage.local.get(["uniqueVisitsCount"]).then((result) => {
  console.log("Value is " + result.uniqueVisitsCount);
});
