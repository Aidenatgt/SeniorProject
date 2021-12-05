from lib.keyboard import KeyboardController
from robot.commands import ReleaseKeyboard, SetVelocity, StopAxis
import sys

betaPos = SetVelocity("Positive Beta Velocity", "beta", 50.0)
betaNeg = SetVelocity("Negative Beta Velocity", "beta", -50.0)
stopBeta = StopAxis("Beta Stop", "beta")

alphaPos = SetVelocity("Positive Alpha Velocity", "alpha", 50.0)
alphaNeg = SetVelocity("Negative Alpha Velocity", "alpha", -50.0)
stopAlpha = StopAxis("Alpha Stop", "alpha")

distPos = SetVelocity("Positive Dist Velocity", "dist", 2.0)
distNeg = SetVelocity("Negative Dist Velocity", "dist", -2.0)
stopDist = StopAxis("Dist Stop", "dist")

pitchPos = SetVelocity("Positive Pitch Velocity", "pitch", 15.0)
pitchNeg = SetVelocity("Negative Pitch Velocity", "pitch", -15.0)
stopPitch = StopAxis("Pitch Stop", "pitch")

rollPos = SetVelocity("Positive Roll Velocity", "roll", 45.0)
rollNeg = SetVelocity("Negative Roll Velocity", "roll", -45.0)
stopRoll = StopAxis("Roll Stop", "roll")

clawPos = SetVelocity("Positive Claw Velocity", "claw", 0.5)
clawNeg = SetVelocity("Negative Claw Velocity", "claw", -0.5)
stopClaw = StopAxis("Claw Stop", "claw")

release_keyboard = ReleaseKeyboard("Release Keyboard")

kb = KeyboardController.getInstance()

kb.whenPressed('w', betaPos)
kb.whenReleased('w', stopBeta)
kb.whenPressed('s', betaNeg)
kb.whenReleased('s', stopBeta)

kb.whenPressed('a', alphaPos)
kb.whenReleased('a', stopAlpha)
kb.whenPressed('d', alphaNeg)
kb.whenReleased('d', stopAlpha)

kb.whenPressed('q', distNeg)
kb.whenReleased('q', stopDist)
kb.whenPressed('e', distPos)
kb.whenReleased('e', stopDist)

kb.whenPressed('i', pitchPos)
kb.whenReleased('i', stopPitch)
kb.whenPressed('k', pitchNeg)
kb.whenReleased('k', stopPitch)

kb.whenPressed('j', rollPos)
kb.whenReleased('j', stopRoll)
kb.whenPressed('l', rollNeg)
kb.whenReleased('l', stopRoll)

kb.whenPressed('u', clawPos)
kb.whenReleased('u', stopClaw)
kb.whenPressed('o', clawNeg)
kb.whenReleased('o', stopClaw)

kb.whenPressed('esc', release_keyboard)