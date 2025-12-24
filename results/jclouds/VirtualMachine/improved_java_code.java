/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.jclouds.azurecompute.arm.domain;

import java.util.Map;

import org.jclouds.javax.annotation.Nullable;
import org.jclouds.json.SerializedNames;

import com.google.auto.value.AutoValue;
import com.google.common.collect.ImmutableMap;

/**
 * A virtual machine  that is valid for your subscription.
 */
@AutoValue
public abstract class VirtualMachineConfiguration {

   /**
    * The identifier of the virtual machine configuration.
    */
   public abstract String virtualMachineConfigurationId();

   /**
    * The name of the virtual machine configuration.
    */
   public abstract String name();

   /**
    * The type of the virtual machine configuration.
    */
   public abstract String virtualMachineConfigurationType();

   /**
    * The location of the virtual machine configuration.
    */
   public abstract String location();

   /**
    * Specifies the tags of the virtual machine configuration.
    */
   @Nullable
   public abstract Map<String, String> tags();

   /**
    * Specifies the properties of the virtual machine configuration.
    */
   public abstract VirtualMachineProperties properties();

   /**
    * Specifies the plan, for marketplace images.
    */
   @Nullable
   public abstract Plan plan();

   @SerializedNames({"virtualMachineConfigurationId", "name", "virtualMachineConfigurationType", "location", "tags", "properties", "plan"})
   public static VirtualMachineConfiguration create(final String virtualMachineConfigurationId, final String name, final String virtualMachineConfigurationType, final String location,
                                                     @Nullable final Map<String, String> tags, VirtualMachineProperties properties, @Nullable Plan plan) {
      return builder().virtualMachineConfigurationId(virtualMachineConfigurationId).name(name).virtualMachineConfigurationType(virtualMachineConfigurationType).location(location).tags(tags).properties(properties).plan(plan)
         .build();
   }

   public abstract Builder toBuilder();

   public static Builder builder() {
      return new AutoValue_VirtualMachineConfiguration.Builder();
   }

   @AutoValue.Builder
   public abstract static class Builder {

      public abstract Builder virtualMachineConfigurationId(String virtualMachineConfigurationId);
      public abstract Builder name(String name);
      public abstract Builder virtualMachineConfigurationType(String virtualMachineConfigurationType);
      public abstract Builder location(String location);
      public abstract Builder tags(Map<String, String> tags);
      public abstract Builder properties(VirtualMachineProperties properties);
      public abstract Builder plan(Plan plan);

      abstract Map<String, String> tags();

      abstract VirtualMachineConfiguration autoBuild();

      public VirtualMachineConfiguration build() {
         tags(tags() != null ? ImmutableMap.copyOf(tags()) : null);
         return autoBuild();
      }
   }
}

@AutoValue
public abstract class VirtualMachine {

   /**
    * Creates a new virtual machine with the given configuration.
    */
   public static VirtualMachine create(VirtualMachineConfiguration configuration) {
      return configuration.toBuilder().build();
   }

   /**
    * The id of the virtual machine.
    */
   public abstract String id();

   /**
    * The name of the virtual machine
    */
   public abstract String name();

   /**
    * The type of the virtual machine .
    */
   public abstract String type();

   /**
    * The localized name of the virtual machine .
    */
   public abstract String location();

   /**
    * Specifies the tags of the vm
    */
   @Nullable
   public abstract Map<String, String> tags();

   /**
    * Specifies the properties of the vm
    */
   public abstract VirtualMachineProperties properties();

   /**
    * Specifies the plan, for marketplace images
    */
   @Nullable
   public abstract Plan plan();

   public abstract Builder toBuilder();

   public static Builder builder() {
      return new AutoValue_VirtualMachine.Builder();
   }

   @AutoValue.Builder
   public abstract static class Builder {

      public abstract Builder id(String id);
      public abstract Builder name(String name);
      public abstract Builder type(String type);
      public abstract Builder location(String location);
      public abstract Builder tags(Map<String, String> tags);
      public abstract Builder properties(VirtualMachineProperties properties);
      public abstract Builder plan(Plan plan);

      abstract Map<String, String> tags();

      abstract VirtualMachine autoBuild();

      public VirtualMachine build() {
         tags(tags() != null ? ImmutableMap.copyOf(tags()) : null);
         return autoBuild();
      }
   }
}