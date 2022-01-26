const takeFirstSlice = require("./main")

describe("takeFirstSlice", () => {
  it("should return 5% of the number", () => {
    expect(takeFirstSlice(100)).toBe(5)
    expect(takeFirstSlice(250)).toBe(12.5)
  })
})
