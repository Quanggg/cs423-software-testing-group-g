const calculateValue = require('../src/CalculateValue')

describe('calculateValue function', () => {
  it('should return value of 30 when adding 10 and 20', () => {
    const result = calculateValue(10, 20)
    expect(result.value).toBe(30)
    expect(result.message).toBeNull()
  })
})
