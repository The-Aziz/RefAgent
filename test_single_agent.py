#!/usr/bin/env python3
"""Quick test to verify agents are working with Groq"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from settings import Settings
from refAgent.agents import PlannerAgent, RefactoringGeneratorAgent

config = Settings()

print(f"Testing Groq integration with model: {config.GROQ_MODEL}")
print(f"API Key exists: {bool(config.GROQ_API_KEY)}")

# Test code
java_code = """
public class TestClass {
    private String name;
    private int age;
    private String email;
    private String address;
    private String phone;
    
    public TestClass() {}
    
    public void setName(String n) { this.name = n; }
    public String getName() { return name; }
    
    public void setAge(int a) { this.age = a; }
    public int getAge() { return age; }
    
    public void setEmail(String e) { this.email = e; }
    public String getEmail() { return email; }
    
    public void setAddress(String a) { this.address = a; }
    public String getAddress() { return address; }
    
    public void setPhone(String p) { this.phone = p; }
    public String getPhone() { return phone; }
}
"""

print("\n=== Testing PlannerAgent ===")
try:
    planner = PlannerAgent(
        api_key=config.GROQ_API_KEY,
        model=config.GROQ_MODEL,
        provider='groq'
    )
    
    print("Planner initialized. Calling analyze_methods()...")
    result = planner.analyze_methods(java_code, "Analyze this test class for refactoring opportunities")
    print(f"✅ SUCCESS! Got response: {result[:200] if result else 'None'}...")
    
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n=== Testing RefactoringGeneratorAgent ===")
try:
    gen = RefactoringGeneratorAgent(
        api_key=config.GROQ_API_KEY,
        model=config.GROQ_MODEL,
        provider='groq'
    )
    
    print("Generator initialized. Calling run()...")
    result = gen.run(f"Refactor this class by using a builder pattern:\n{java_code}", use_refactoring_generator_prompt=True)
    print(f"✅ SUCCESS! Got response: {result[:200] if result else 'None'}...")
    
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n✅ Agent test complete!")
